from celery import shared_task
from .models import Scan, ScanDetectedBook, Book
from PIL import Image
import pytesseract
from django.utils import timezone

@shared_task
def process_scan(scan_id):
    try:
        scan = Scan.objects.get(id=scan_id)
        scan.status = "processing"
        scan.save()

        # Open image
        image_path = scan.image.path
        img = Image.open(image_path)

        # Run OCR
        ocr_result = pytesseract.image_to_string(img)

        # Split text by line
        lines = [line.strip() for line in ocr_result.split("\n") if line.strip()]

        # For MVP: assume each line is a book title
        for line in lines:
            book, created = Book.objects.get_or_create(title=line, defaults={"author": "Unknown"})
            ScanDetectedBook.objects.create(scan=scan, book=book, confidence_score=0.9)

        scan.status = "completed"
        scan.processed_at = timezone.now()
        scan.save()

        return {"status": "success", "scan_id": scan.id, "books_detected": len(lines)}

    except Exception as e:
        scan.status = "failed"
        scan.save()
        return {"status": "failed", "error": str(e), "scan_id": scan_id}