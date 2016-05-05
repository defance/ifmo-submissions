from submissions.serializers import (
    SubmissionSerializer, StudentItemSerializer, ScoreSerializer
)
from ifmo_submissions.serializers import ScoreAnnotationSerializer
from submissions.models import Submission, StudentItem, Score, ScoreAnnotation, ScoreSummary


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


def get_annotation(student_item):
    """Get the annotation for a particular student item

    This function will return the annotation if it is available.

    Args:
        student_item (dict): The dictionary representation of a student item.
            Function returns the annotation related to this student item.

    Returns:
        annotation (dict): The annotation associated with this student item.
            None if there is no annotation found.

    Raises:
        SubmissionInternalError: Raised if a score cannot be retrieved because
            of an internal server error.
    """
    try:
        student_item_model = StudentItem.objects.get(**student_item)
        score = ScoreSummary.objects.get(student_item=student_item_model).latest
        annotation = ScoreAnnotation.objects.get(score=score)
    except (ScoreSummary.DoesNotExist, StudentItem.DoesNotExist, ScoreAnnotation.DoesNotExist):
        return None

    # By convention, scores are hidden if "points possible" is set to 0.
    # This can occur when an instructor has reset scores for a student.
    if score.is_hidden():
        return None
    else:
        return ScoreAnnotationSerializer(annotation).data
