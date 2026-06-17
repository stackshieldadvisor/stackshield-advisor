import unittest


class DeploymentScriptTests(unittest.TestCase):
    def test_deployment_defaults_match_github_project_pages(self):
        from scripts import deploy_github_pages

        self.assertEqual(
            deploy_github_pages.BASE_URL,
            "https://stackshieldadvisor.github.io/stackshield-advisor",
        )
        self.assertEqual(deploy_github_pages.PATH_PREFIX, "/stackshield-advisor")
        self.assertEqual(deploy_github_pages.REMOTE_URL, "https://github.com/stackshieldadvisor/stackshield-advisor.git")
        self.assertEqual(deploy_github_pages.PUBLIC_URL, "https://stackshieldadvisor.github.io/stackshield-advisor/")

    def test_sanitize_output_redacts_github_tokens(self):
        from scripts.deploy_github_pages import sanitize_output

        fake_fine_grained = "github" + "_pat_" + ("A" * 30)
        fake_classic = "ghp_" + ("B" * 36)
        raw = f"failed with {fake_fine_grained} and {fake_classic}"
        sanitized = sanitize_output(raw)

        self.assertNotIn(fake_fine_grained, sanitized)
        self.assertNotIn(fake_classic, sanitized)
        self.assertEqual(sanitized.count("[REDACTED_GITHUB_TOKEN]"), 2)


if __name__ == "__main__":
    unittest.main()
