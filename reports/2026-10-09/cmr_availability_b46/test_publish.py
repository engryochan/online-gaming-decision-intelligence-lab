import subprocess, unittest
from publish import execute

class PublicationFailureTests(unittest.TestCase):
    def verify_failure(self, fail_command):
        seen=[]
        def runner(command, **kwargs):
            self.assertTrue(kwargs['check'])
            seen.append(command[0])
            if command[0] == fail_command:
                raise subprocess.CalledProcessError(1, command)
        with self.assertRaises(subprocess.CalledProcessError):
            execute([['verify'], ['commit'], ['push']], runner=runner)
        return seen

    def test_rejected_verification_prevents_commit_and_push(self):
        self.assertEqual(self.verify_failure('verify'), ['verify'])

    def test_failed_commit_prevents_push(self):
        self.assertEqual(self.verify_failure('commit'), ['verify','commit'])

if __name__ == '__main__':
    unittest.main()
