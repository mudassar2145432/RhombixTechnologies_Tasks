

  output "api_url" {
  description = "Full endpoint URL for the AddBloodDeposit route"
  value       = "${aws_apigatewayv2_api.api.api_endpoint}/${aws_apigatewayv2_stage.stage.name}/AddBloodDeposit"
}

