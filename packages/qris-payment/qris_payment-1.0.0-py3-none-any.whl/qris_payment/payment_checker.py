import requests
from datetime import datetime, timedelta

class PaymentChecker:
    def __init__(self, config):
        self.config = {
            'merchant_id': config.get('merchant_id'),
            'api_key': config.get('api_key')
        }

    def check_payment_status(self, reference, amount):
        try:
            response = requests.get(
                f"https://gateway.okeconnect.com/api/mutasi/qris/{self.config['merchant_id']}/{self.config['api_key']}"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == "success" and data.get('data'):
                    transactions = data['data']
                    matching_transactions = [
                        tx for tx in transactions
                        if (int(tx['amount']) == amount and
                            tx['qris'] == "static" and
                            tx['type'] == "CR" and
                            (datetime.now() - datetime.strptime(tx['date'], '%Y-%m-%d %H:%M:%S')).total_seconds() <= 300)
                    ]
                    
                    if matching_transactions:
                        latest_transaction = max(
                            matching_transactions,
                            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S')
                        )
                        
                        return {
                            'success': True,
                            'data': {
                                'status': 'PAID',
                                'amount': int(latest_transaction['amount']),
                                'reference': latest_transaction['issuer_reff'],
                                'date': latest_transaction['date'],
                                'brand_name': latest_transaction['brand_name'],
                                'buyer_reff': latest_transaction['buyer_reff']
                            }
                        }
            
            return {
                'success': True,
                'data': {
                    'status': 'UNPAID',
                    'amount': amount,
                    'reference': reference
                }
            }
            
        except Exception as e:
            raise Exception(f"Gagal cek status pembayaran: {str(e)}") 