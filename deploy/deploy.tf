variable "config" {
    default = {
        vpc_id = "vpc-b91664dc"
        key_name = "mperrone"
        ami = "ami-74425015"
        app_name = "rank"
    }
}

provider "aws" {
    region = "us-west-2"
}

resource "aws_launch_configuration" "server-launch-conf" {
    image_id = "${var.config.ami}"
    instance_type = "t2.micro"
    security_groups = ["${aws_security_group.allow_http.name}"]
    key_name = "${var.config.key_name}"
}

resource "aws_elb" "rankelb" {
    name = "${var.config.app_name}"
    availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]

    listener {
        instance_port = 80
        instance_protocol = "http"
        lb_port = 80
        lb_protocol = "http"
    }

    health_check {
        healthy_threshold = 2
        unhealthy_threshold = 4
        timeout = 3
        target = "HTTP:80/api/health"
        interval = 30
    }

    cross_zone_load_balancing = true
    idle_timeout = 400
    connection_draining = true
    connection_draining_timeout = 400

    tags {
        Name = "${var.config.app_name}"
    }
}
resource "aws_autoscaling_group" "server-group" {
    name = "${var.config.app_name}-server-group"
    min_size = 2
    max_size = 10
    health_check_type = "ELB"
    health_check_grace_period = 100
    availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]
    launch_configuration = "${aws_launch_configuration.server-launch-conf.name}"
    load_balancers = ["${aws_elb.rankelb.name}"]
}

resource "aws_autoscaling_policy" "scale-up-policy" {
    name = "${var.config.app_name}-scale-up-policy"
    scaling_adjustment = 2
    adjustment_type = "ChangeInCapacity"
    cooldown = 300
    autoscaling_group_name = "${aws_autoscaling_group.server-group.name}"
}

resource "aws_cloudwatch_metric_alarm" "cpu-overusage-alarm" {
    alarm_name = "${var.config.app_name}-cpu-overusage-alarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    threshold = "85"
    evaluation_periods = "2"
    metric_name = "CPUUtilization"
    namespace = "AWS/EC2"
    period = "60"
    statistic = "Average"
    dimensions {
        AutoScalingGroupName = "${aws_autoscaling_group.server-group.name}"
    }
    alarm_description = "This metric monitors cpu over-utilization"
    alarm_actions = ["${aws_autoscaling_policy.scale-up-policy.arn}"]
}

resource "aws_autoscaling_policy" "scale-down-policy" {
    name = "${var.config.app_name}-scale-down-policy"
    scaling_adjustment = -1
    adjustment_type = "ChangeInCapacity"
    cooldown = 300
    autoscaling_group_name = "${aws_autoscaling_group.server-group.name}"
}

resource "aws_cloudwatch_metric_alarm" "cpu-underusage-alarm" {
    alarm_name = "${var.config.app_name}-cpu-underusage-alarm"
    comparison_operator = "LessThanOrEqualToThreshold"
    threshold = "55"
    evaluation_periods = "2"
    metric_name = "CPUUtilization"
    namespace = "AWS/EC2"
    period = "60"
    statistic = "Average"
    dimensions {
        AutoScalingGroupName = "${aws_autoscaling_group.server-group.name}"
    }
    alarm_description = "This metric monitors cpu under-utilization"
    alarm_actions = ["${aws_autoscaling_policy.scale-down-policy.arn}"]
}

resource "aws_route53_record" "www" {
    zone_id = "Z2K9PS3Q3T79U7"
    name = "tmwild.com"
    type = "A"
    alias {
        name = "${aws_elb.rankelb.dns_name}"
        zone_id = "${aws_elb.rankelb.zone_id}"
        evaluate_target_health = false
    }
}
