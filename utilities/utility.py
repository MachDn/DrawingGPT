import boto3

class Utility:
    def upload_image():
        return 'upload placeholder'
        s3 = boto3.client(
                            aws_access_key_id=config['AWS']['aws_access_key_id'],
                            aws_secret_access_key=config['AWS']['aws_secret_access_key'],
                            aws_session_token="IQoJb3JpZ2luX2VjENT//////////wEaDmFwLW5vcnRoZWFzdC0yIkgwRgIhAP7cNM+olk2fDAw54uqRnla62foKBxXJYd+l3t8qshu+AiEAlMvNlLjHnmb6IzFyUa+Marb2HmCJzuODNZnCUp72d+oq6wEIbRAAGgwwODg4NzMyMDYwNDUiDP3EFmh2pQ7hFKpDiirIAbK1QlbnZS1Nur+Mhowb+CayPUhN3X0o1vqRFABmWtS4Nj1VtRxXhatnqujeGwrb6m2XqyiHvXSQ1X6xWa8Seb76peT2gY25hmH9OclE9wDlzI2VtyvM7NnM2ZRhhF+k3c/6xbl1JsU+mASAB/CMtWnFD0aqpmuMadEDpqmsPZixKSlr6y/kqSjaCXLuqi/KwfktM+fwKP7a/whP85DQj58M1TrTNvz4NOCszqfv5IYJZS8WYHaR7NXB0dK9fwDHr+M+oEagFoiYMKWbwZ8GOpcBx2ewKJ4CXfclX4EYH/fcAnkdDpY5W+VpfvYots6t6mwY19f8NeOv3NTcKBBWkEqv9q7UtNYUyuxpdWJccKqMVfEF0zYQb+Qrp5sFmaa3z+PopTHUilmxylP7+EdJjfZuGPthUJx6TGsP9JA6/DacYywo3ZY9mP0W/r0uymBxNrhp15z/K7xLqKAaPA8TnjeN/a3nohEzqQ=="
                            )
        BUCKET_NAME='fal-front'