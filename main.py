from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class CalculationRequest(BaseModel):
    a: float
    b: float

@app.get("/", response_class=HTMLResponse)
async def calculator_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Web Calculator</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; margin-top: 50px; }
            input { margin: 5px; padding: 10px; font-size: 16px; }
            button { margin: 5px; padding: 10px; font-size: 16px; cursor: pointer; }
            #result { margin-top: 20px; font-size: 20px; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Calculator</h1>
        <input id="num1" type="number" placeholder="Enter first number" />
        <input id="num2" type="number" placeholder="Enter second number" />
        
        <div>
            <button onclick="calculate('add')">Add</button>
            <button onclick="calculate('subtract')">Subtract</button>
            <button onclick="calculate('multiply')">Multiply</button>
            <button onclick="calculate('divide')">Divide</button>
        </div>
        
        <div id="result"></div>
        
        <script>
            async function calculate(operation) {
                const num1 = parseFloat(document.getElementById('num1').value);
                const num2 = parseFloat(document.getElementById('num2').value);
                const response = await fetch(`/${operation}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ a: num1, b: num2 })
                });
                const data = await response.json();
                if (response.ok) {
                    document.getElementById('result').textContent = `Result: ${data.result}`;
                } else {
                    document.getElementById('result').textContent = `Error: ${data.detail}`;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/add")
async def add(request: CalculationRequest):
    return {"result": request.a + request.b}

@app.post("/subtract")
async def subtract(request: CalculationRequest):
    return {"result": request.a - request.b}

@app.post("/multiply")
async def multiply(request: CalculationRequest):
    return {"result": request.a * request.b}

@app.post("/divide")
async def divide(request: CalculationRequest):
    if request.b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero.")
    return {"result": request.a / request.b}
