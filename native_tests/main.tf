resource "aws_dynamodb_table" "blog_posts" {
  name           = "BlogPosts"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PKEY"

  attribute {
    name = "PKEY"
    type = "S"
  }
}

output "dynamo_table_name" {
  value = aws_dynamodb_table.blog_posts.name
}
