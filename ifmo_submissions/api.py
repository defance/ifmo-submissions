from submissions.serializers import (
    SubmissionSerializer, StudentItemSerializer, ScoreSerializer
)
from ifmo_submissions.serializers import ScoreAnnotationSerializer
from submissions.models import Submission, StudentItem, Score, ScoreAnnotation


def get_submission_annotation(student_item, attempt_number):

    # TODO: Docs
    try:
        student_item_model = StudentItem.objects.get(**student_item)
        submission = Submission.objects.get(student_item=student_item_model,
                                            attempt_number=attempt_number)
        score = None
        annotation = None

        try:
            score = Score.objects.filter(
                student_item=student_item_model,
                submission=submission).order_by("-id").first()
        except Score.DoesNotExist:
            pass

        if score is not None:
            try:
                annotation = ScoreAnnotation.objects.get(score=score)
            except ScoreAnnotation.DoesNotExist:
                pass

    except StudentItem.DoesNotExist, Submission.DoesNotExist:
        return None

    return {
        'student_module': StudentItemSerializer(student_item_model).data,
        'submission': SubmissionSerializer(submission).data,
        'score': ScoreSerializer(score).data if score is not None else None,
        'annotation': ScoreAnnotationSerializer(annotation).data if annotation is not None else None,
    }


def get_submission_annotation_uuid(uuid):

    # TODO: Docs
    try:
        submission = Submission.objects.get(uuid=uuid)
        student_item_model = submission.student_item
        score = None
        annotation = None

        try:
            score = Score.objects.filter(
                student_item=student_item_model,
                submission=submission).order_by("-id").first()
        except Score.DoesNotExist:
            pass

        if score is not None:
            try:
                annotation = ScoreAnnotation.objects.get(score=score)
            except ScoreAnnotation.DoesNotExist:
                pass

    except StudentItem.DoesNotExist, Submission.DoesNotExist:
        return None

    return {
        'student_module': StudentItemSerializer(student_item_model).data,
        'submission': SubmissionSerializer(submission).data,
        'score': ScoreSerializer(score).data if score is not None else None,
        'annotation': ScoreAnnotationSerializer(annotation).data if annotation is not None else None,
    }

