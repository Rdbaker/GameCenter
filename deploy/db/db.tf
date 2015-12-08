variable "pgpass" {}

provider "aws" {
    region = "us-west-2"
}

resource "aws_security_group" "allow_db" {
  name = "allow_db"
  description = "Allow all db traffic"

  ingress {
      from_port = 5432
      to_port = 5432
      protocol = "TCP"
      cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_db_instance" "rankdb" {
    identifier = "rankdb"
    allocated_storage = 10
    engine = "postgres"
    engine_version = "9.4.4"
    instance_class = "db.t2.micro"
    name = "rankdb"
    username = "rankuser"
    password = "${var.pgpass}"
    vpc_security_group_ids = ["${aws_security_group.allow_db.id}"]
}
