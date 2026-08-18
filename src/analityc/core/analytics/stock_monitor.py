class StockMonitor:
    def __init__(self, product_class_id=1, threshold=5):
        self.product_class_id = product_class_id
        self.threshold = threshold

    def monitor(self, detections):
        """
        detections: List of dicts with 'class_id'
        """
        product_count = sum(1 for d in detections if d.get('class_id') == self.product_class_id)
        
        return {
            "product_count": product_count,
            "status": "OK" if product_count >= self.threshold else "LOW_STOCK"
        }
