provider "aws" {
  region = var.region
}

# 1. Create DynamoDB table
resource "aws_dynamodb_table" "blood_bank_table" {
  name           = "BloodBankTable"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "deposit_id"

  attribute {
    name = "deposit_id"
    type = "S"
  }
}

# 2. IAM Role for Lambda
resource "aws_iam_role" "lambda_exec" {
  name = "blood_bank_lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# 3. Attach policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# 4. Archive Lambda function
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "lambda/lambda_function.py"
  output_path = "lambda_function.zip"
}

# 5. Create Lambda function
resource "aws_lambda_function" "blood_bank_lambda" {
  function_name    = "BloodBankLambdaFunction"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}

# 6. API Gateway HTTP API with CORS enabled
resource "aws_apigatewayv2_api" "api" {
  name          = "BloodBankAPI"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins     = ["*"]
    allow_methods     = ["POST"]
    allow_headers     = ["content-type"]
    expose_headers    = []
    max_age           = 3600
    allow_credentials = false
  }
}

# 7. API Integration with Lambda
resource "aws_apigatewayv2_integration" "lambda" {
  api_id                = aws_apigatewayv2_api.api.id
  integration_type      = "AWS_PROXY"
  integration_uri       = aws_lambda_function.blood_bank_lambda.invoke_arn
  integration_method    = "POST"
  payload_format_version = "2.0"
}

# 8. API Route
resource "aws_apigatewayv2_route" "route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /AddBloodDeposit"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# 9. API Stage with auto deploy
resource "aws_apigatewayv2_stage" "stage" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "prod"
  auto_deploy = true
}

# 10. Lambda permission for API Gateway
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.blood_bank_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}
