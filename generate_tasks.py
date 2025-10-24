import json
import csv
import re
import subprocess

def get_linked_issues(pr_body):
    """
    Parses a PR body for linked issues.
    Looks for "closes #", "fixes #", and full GitHub issue URLs.
    """
    issues = []
    # Regex to find "closes #123", "fixes #123", or full URLs
    pattern = r'(?i)(?:closes|fixes) #(\d+)|https://github.com/cashapp/misk/issues/(\d+)'
    matches = re.findall(pattern, pr_body)
    for match in matches:
        issue_num = match[0] if match[0] else match[1]
        if issue_num:
            issues.append(f"https://github.com/cashapp/misk/issues/{issue_num}")
    return issues

def get_test_file_count(pr_number):
    try:
        result = subprocess.run(
            ["gh", "pr", "diff", str(pr_number), "--repo", "cashapp/misk", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        return len([line for line in result.stdout.strip().splitlines() if line.endswith("Test.kt")])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0

def get_commit_info(pr_number):
    try:
        result = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--repo", "cashapp/misk", "--json", "mergeCommit"],
            capture_output=True,
            text=True,
            check=True
        )
        merge_commit = json.loads(result.stdout).get("mergeCommit")
        if not merge_commit:
            return None, None

        fix_commit = merge_commit["oid"]

        # Use gh api to get the parent commit
        api_result = subprocess.run(
            ["gh", "api", f"/repos/cashapp/misk/commits/{fix_commit}"],
            capture_output=True,
            text=True,
            check=True
        )
        commit_data = json.loads(api_result.stdout)
        parents = commit_data.get("parents")
        if not (parents and len(parents) > 0):
            return None, None
        base_commit = parents[0].get("sha")
        return fix_commit, base_commit
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, KeyError, IndexError):
        return None, None

def main():
    try:
        result = subprocess.run(
            ["gh", "pr", "list", "--repo", "cashapp/misk", "--state", "closed", "--limit", "1000", "--json", "number,title,url,body"],
            capture_output=True,
            text=True,
            check=True
        )
        prs = json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        print("Failed to fetch pull requests.")
        return

    candidates = []
    for pr in prs:
        if any(keyword in pr["title"].lower() for keyword in ["fix", "bug", "add", "feat", "refactor", "docs"]):
            pr_number = pr["number"]
            print(f"Processing PR #{pr_number}")
            test_file_count = get_test_file_count(pr_number)
            if test_file_count > 0:
                score = 0
                if get_linked_issues(pr["body"]):
                    score += 1
                score += len(pr["body"]) / 1000
                score += test_file_count

                candidates.append({
                    "pr": pr,
                    "score": score
                })

    # Sort candidates by score
    candidates.sort(key=lambda x: x["score"], reverse=True)

    tasks = []
    for candidate in candidates[:10]:
        pr = candidate["pr"]
        pr_number = pr["number"]
        print(f"Adding PR #{pr_number} to tasks.")
        fix_commit, base_commit = get_commit_info(pr_number)
        if fix_commit and base_commit:
            tasks.append({
                "task_rank": len(tasks) + 1,
                "pr_hyperlink": pr["url"],
                "fix_commit": fix_commit,
                "base_commit": base_commit,
                "issue_hyperlink": get_linked_issues(pr["body"])[0] if get_linked_issues(pr["body"]) else ""
            })

    with open("misk_benchmark_tasks.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["task_rank", "pr_hyperlink", "fix_commit", "base_commit", "issue_hyperlink"])
        writer.writeheader()
        writer.writerows(tasks)

    print(f"CSV file created with {len(tasks)} tasks.")

if __name__ == "__main__":
    main()
