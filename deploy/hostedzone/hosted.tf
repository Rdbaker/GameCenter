provider "aws" {
    region = "us-west-2"
}

resource "aws_route53_zone" "tmwild" {
    name = "tmwild.com"
}

output "hosted_zone_id" {
    value = "${aws_route53_zone.tmwild.zone_id}"
}

output "name_servers" {
    value = "${aws_route53_zone.tmwild.name_servers.0},${aws_route53_zone.tmwild.name_servers.1},${aws_route53_zone.tmwild.name_servers.2},${aws_route53_zone.tmwild.name_servers.3}"
}
