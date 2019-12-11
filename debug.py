"""Hemlock debugger"""

from hemlock.debug import AIParticipant, main

if __name__ == '__main__':
    main()

# from app import app
# from hemlock.debug import main, AIParticipantBase
# from unittest import TestCase

# NUM_BATCHES = 1
# BATCH_SIZE = 1

# app.app_context().push()


# class AIParticipant(AIParticipantBase, TestCase):
#     SURVEY_URL = 'http://localhost:5000'

#     def custom_debug_example(self, question):
#         question.send_keys('hello world')

# if __name__ == '__main__':
#     main(NUM_BATCHES, BATCH_SIZE)