locals {
  namespace = random_string.namespace.result
}

resource "random_string" "namespace" {
  length  = 4
  special = false
}

resource "aws_dynamodb_table" "blog_posts" {
  name         = "${local.namespace}-BlogPosts"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PKEY"

  attribute {
    name = "PKEY"
    type = "S"
  }
}

output "dynamo_table_name" {
  value = aws_dynamodb_table.blog_posts.name
}
