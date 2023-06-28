def wait_until_finished(actions, message):
        print(message)
        for a in actions:
                 a.wait_until_finished()
