

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Prediction 


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home_view(request):
    # Show recent predictions on home page
    recent_predictions = Prediction.objects.all()[:5]
    predictions_list = ""
    for pred in recent_predictions:
        predictions_list += f"<li>{pred.prediction} (Confidence: {pred.confidence:.2%}) - {pred.created_at.strftime('%m/%d %H:%M')}</li>"
    
    
    return HttpResponse("""
    <h1>Iris Classification App</h1>
    <p>Welcome to the Iris ML application!</p>
    <ul>
        <li><a href="/iris/predict/">Make a Prediction</a></li>
        <li><a href="/iris/train/">Train Model</a></li>
        <li><a href="/iris/api/predict/?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2">Test API</a></li>
    </ul>
    """)

def predict_iris(request):
    """View for HTML form prediction"""
    if request.method == 'POST':
        # Handle form submission
        try:
            sepal_length = float(request.POST.get('sepal_length', 5.1))
            sepal_width = float(request.POST.get('sepal_width', 3.5))
            petal_length = float(request.POST.get('petal_length', 1.4))
            petal_width = float(request.POST.get('petal_width', 0.2))
            
            # Mock prediction (replace with actual ML model later)
            mock_prediction = "setosa"
            confidence = 0.95
            

        # Save to database
            prediction_record = Prediction.objects.create(
                sepal_length=sepal_length,
                sepal_width=sepal_width,
                petal_length=petal_length,
                petal_width=petal_width,
                prediction=mock_prediction,
                confidence=confidence,
                prediction_type='form'
            )

            return HttpResponse(f"""
            <h2>Prediction Result</h2>
            <div style="background: #e8f4fc; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Prediction:</strong> {mock_prediction}</p>
                <p><strong>Confidence:</strong> {confidence:.2%}</p>
            </div>
            <div style="background: #f9f9f9; padding: 15px; border-radius: 5px;">
                <h3>Input Features:</h3>
                <ul>
                    <li>Sepal Length: {sepal_length} cm</li>
                    <li>Sepal Width: {sepal_width} cm</li>
                    <li>Petal Length: {petal_length} cm</li>
                    <li>Petal Width: {petal_width} cm</li>
                </ul>
            </div>
            <p><a href="/iris/predict/">Make Another Prediction</a></p>
            <p><a href="/iris/">Back to Home</a></p>
            """)
        except Exception as e:
            return HttpResponse(f"<h2>Error</h2><p>{str(e)}</p>")
    
    # Render the form template for GET requests
    return render(request, 'iris_app/predict.html')

@csrf_exempt
def api_predict_iris(request):
    """API endpoint for predictions"""
    if request.method == 'GET':
        try:
            sepal_length = float(request.GET.get('sepal_length', 5.1))
            sepal_width = float(request.GET.get('sepal_width', 3.5))
            petal_length = float(request.GET.get('petal_length', 1.4))
            petal_width = float(request.GET.get('petal_width', 0.2))
            
            # For now, return mock response
            # Later we'll integrate the actual ML model
            mock_prediction = "setosa"
            confidence = 0.95

            # Save to database
            prediction_record = Prediction.objects.create(
                sepal_length=sepal_length,
                sepal_width=sepal_width,
                petal_length=petal_length,
                petal_width=petal_width,
                prediction=mock_prediction,
                confidence=confidence,
                prediction_type='api'
            )
            
            return JsonResponse({
                'prediction': mock_prediction,
                'confidence': confidence,
                'features': {
                    'sepal_length': sepal_length,
                    'sepal_width': sepal_width,
                    'petal_length': petal_length,
                    'petal_width': petal_width,
                },
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'})
    
    return JsonResponse({'error': 'Only GET method allowed', 'status': 'error'})

def train_model(request):
    """View to trigger model training"""
    try:
        # Import your training function (you'll need to create this)
        # from .utils import train_and_save_model
        
        # For now, return a mock training response
        # model, accuracy, model_path = train_and_save_model()
        
        accuracy = 0.95
        model_path = "/models/iris_model.pkl"
        
        return HttpResponse(f"""
        <h2>Model Training Complete!</h2>
        <div style="background: #e8f4fc; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Accuracy:</strong> {accuracy:.2%}</p>
            <p><strong>Model saved at:</strong> {model_path}</p>
        </div>
        <p><a href="/iris/predict/">Go to Prediction</a></p>
        <p><a href="/iris/">Back to Home</a></p>
        """)
    except Exception as e:
        return HttpResponse(f"""
        <h2>Training Failed</h2>
        <div style="background: #ffe8e8; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Error:</strong> {str(e)}</p>
        </div>
        <p><a href="/iris/">Back to Home</a></p>
        """)
    
    # NEW: Add a view to see prediction history
def prediction_history(request):
    """View to show all predictions"""
    predictions = Prediction.objects.all()
    
    predictions_html = ""
    for pred in predictions:
        predictions_html += f"""
        <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <h4>Prediction #{pred.id} - {pred.prediction}</h4>
            <p><strong>Confidence:</strong> {pred.confidence:.2%}</p>
            <p><strong>Type:</strong> {pred.get_prediction_type_display()}</p>
            <p><strong>Date:</strong> {pred.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Features:</strong> SL: {pred.sepal_length}, SW: {pred.sepal_width}, PL: {pred.petal_length}, PW: {pred.petal_width}</p>
        </div>
        """
    
    return HttpResponse(f"""
    <h1>Prediction History</h1>
    <p><a href="/iris/">← Back to Home</a></p>
    <div style="margin: 20px 0;">
        {predictions_html if predictions else "<p>No predictions recorded yet.</p>"}
    </div>
    <p><a href="/iris/">← Back to Home</a></p>
    """)