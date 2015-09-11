# Copyright 2015 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
    This module contains constants to be used for testing the behavior
    of the parser against various CFN template scenarios.
"""


# DUMMY_TEST_TEMPLATE contains the bare minimum of fields required of a
# template. It is useful in tests which do not depend on the data
# of the input template itself.
DUMMY_TEST_TEMPLATE = """
{
    "Parameters": {},
    "Resources": {}
}
"""[1:]

# PROCESSED_TEST_TEMPLATE contains the data of a template which contains no
# actual templating function usage. It useful for testing aspects which
# imply using an already processed template.
PROCESSED_TEST_TEMPLATE = """
{
    "Parameters": {
        "SimpleParam": {
            "Default": "SimpleString"
        },
        "AdvancedParam": {
            "Default": ["An", "unexpected", "list"]
        },
        "NoDefault": {
            "Description": "Has no 'Default' field"
        },
        "ResourceParam": {
            "Default": "prioritised"
        }
    },

    "Mappings": {
        "ExampleMapping": {
            "good": { "goodval": "some value" },
            "bad": "this ain't good..."
        }
    },

    "Resources": {
        "DummyResource": {
            "Type": "SOME::RES::TYPE",
            "Properties": {
                "Prop1": "value 1",
                "Prop2": "value 2",
                "ListProp": ["this", "is", "a", "list"],
                "DictProp": {
                    "key1": "val1",
                    "key2": "val2"
                },
                "NestedProp": {
                    "NestedString": "A string",
                    "NestedList": ["val1", {"key1": "val1"}, "val3"],
                    "NestedInt": 5,
                    "NestedDict": {
                        "key1": "val1",
                        "list": [1, 2, 3]
                    }
                }
            }
        },
        "ResourceParam": {}
    }
}
"""[1:]


# COMPLETE_TEST_TEMPLATE contains the raw data of a template to be used
# advanced parsing behavioral tests.
COMPLETE_TEST_TEMPLATE = """
{
  "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "AWS CloudFormation Sample Template WordPress_Single_Instance: WordPress is web software you can use to create a beautiful website or blog. This template installs a single-instance WordPress deployment using a local MySQL database to store the data.",

  "Parameters" : {

    "KeyName" : {
      "Description" : "Name of an existing EC2 KeyPair to enable SSH access to the instances",
      "Type" : "String"
    },

    "InstanceType" : {
      "Description" : "WikiServer EC2 instance type",
      "Type" : "String",
      "Default" : "m1.small",
      "AllowedValues" : [ "m1.tiny", "m1.small", "m1.medium", "m1.large", "m1.xlarge" ],
      "ConstraintDescription" : "must be a valid EC2 instance type."
    },

    "VolumeSize" : {
      "Description" : "WikiServer Volume size",
      "Type" : "Number",
      "Default" : "1",
      "MinValue" : "1",
      "MaxValue" : "1024",
      "ConstraintDescription" : "must be between 1 and 1024 Gb."
    },

    "DBName": {
      "Default": "wordpress",
      "Description" : "The WordPress database name",
      "Type": "String",
      "MinLength": "1",
      "MaxLength": "64",
      "AllowedPattern" : "[a-zA-Z][a-zA-Z0-9]*",
      "ConstraintDescription" : "must begin with a letter and contain only alphanumeric characters."
    },

    "DBUsername": {
      "Default": "admin",
      "NoEcho": "true",
      "Description" : "The WordPress database admin account username",
      "Type": "String",
      "MinLength": "1",
      "MaxLength": "16",
      "AllowedPattern" : "[a-zA-Z][a-zA-Z0-9]*",
      "ConstraintDescription" : "must begin with a letter and contain only alphanumeric characters."
    },

    "DBPassword": {
      "Default": "admin",
      "NoEcho": "true",
      "Description" : "The WordPress database admin account password",
      "Type": "String",
      "MinLength": "1",
      "MaxLength": "41",
      "AllowedPattern" : "[a-zA-Z0-9]*",
      "ConstraintDescription" : "must contain only alphanumeric characters."
    },

    "DBRootPassword": {
      "Default": "admin",
      "NoEcho": "true",
      "Description" : "Root password for MySQL",
      "Type": "String",
      "MinLength": "1",
      "MaxLength": "41",
      "AllowedPattern" : "[a-zA-Z0-9]*",
      "ConstraintDescription" : "must contain only alphanumeric characters."
    },
    "LinuxDistribution": {
      "Default": "F17",
      "Description" : "Distribution of choice",
      "Type": "String",
      "AllowedValues" : [ "F17" ]
    }
  },

  "Mappings" : {
    "AWSInstanceType2Arch" : {
      "m1.tiny"    : { "Arch" : "32" },
      "m1.small"    : { "Arch" : "64" },
      "m1.medium"    : { "Arch" : "64" },
      "m1.large"   : { "Arch" : "64" },
      "m1.xlarge"   : { "Arch" : "64" }
    },
    "DistroArch2AMI": {
      "F17"      : { "32" : "F17-i386-cfntools", "64" : "F17-x86_64-cfntools" }
    }
  },

  "Resources" : {

    "IPAddress" : {
      "Type" : "AWS::EC2::EIP"
    },

    "IPAssoc" : {
      "Type" : "AWS::EC2::EIPAssociation",
      "Properties" : {
        "InstanceId" : { "Ref" : "WikiServer" },
        "EIP" : { "Ref" : "IPAddress" }
      }
    },
    "WikiServerSecurityGroup" : {
      "Type" : "AWS::EC2::SecurityGroup",
      "Properties" : {
        "GroupDescription" : "Deny HTTP access via port 80 but allow SSH access",
        "SecurityGroupIngress" : [
          {"IpProtocol" : "tcp", "FromPort" : "22", "ToPort" : "22", "CidrIp" : "0.0.0.0/0"}
        ],
        "SecurityGroupEgress": [
          {"IpProtocol" : "tcp", "FromPort" : "80", "ToPort" : "80", "CidrIp" : "0.0.0.0/0"}
        ]
      }
    },

    "WikiServer": {
      "Type": "AWS::EC2::Instance",
      "Metadata" : {
        "AWS::CloudFormation::Init" : {
          "config" : {
            "packages" : {
              "yum" : {
                "httpd"        : [],
                "mysql"        : [],
                "mysql-server" : [],
                "wordpress"    : []
              }
            },
            "services" : {
              "systemd" : {
                "httpd"    : { "enabled" : "true", "ensureRunning" : "true" },
                "mysqld"   : { "enabled" : "true", "ensureRunning" : "true" }
              }
            }
          }
        }
      },
      "Properties": {
        "ImageId" : { "Fn::FindInMap" : [ "DistroArch2AMI", { "Ref" : "LinuxDistribution" },
                          { "Fn::FindInMap" : [ "AWSInstanceType2Arch", { "Ref" : "InstanceType" }, "Arch" ] } ] },
        "InstanceType"   : { "Ref" : "InstanceType" },
        "KeyName"        : { "Ref" : "KeyName" },
        "SecurityGroups" : [ {"Ref" : "WikiServerSecurityGroup"} ],
        "UserData"       : { "Fn::Base64" : { "Fn::Join" : ["", [
          "#!/bin/bash -v\\n",
          "/opt/aws/bin/cfn-init\\n",
          "# Wait for the volume to appear\\n",
          "while [ ! -e /dev/vdc ]; do echo Waiting for volume to attach; sleep 1; done\\n",
          "parted -s /dev/vdc mklabel msdos\\n",
          "parted -s /dev/vdc mkpart primary ext3 1 1000\\n",
          "# Format the EBS volume and mount it\\n",
          "systemctl stop mysqld.service\\n",
          "sleep 1\\n",
          "mv /var/lib/mysql /var/lib/mysql.data\\n",
          "/sbin/mkfs -t ext3 /dev/vdc1\\n",
          "mkdir /var/lib/mysql\\n",
          "mount /dev/vdc1 /var/lib/mysql\\n",
          "chown mysql.mysql /var/lib/mysql\\n",
          "mv -n /var/lib/mysql.data/* /var/lib/mysql\\n",
          "systemctl start mysqld.service\\n",
          "sleep 1\\n",
          "# Setup MySQL root password and create a user\\n",
          "mysqladmin -u root password ", { "Ref" : "DBRootPassword" }, "\\n",
          "cat << EOF | mysql -u root --password=", { "Ref" : "DBRootPassword" }, "\\n",
          "CREATE DATABASE ", { "Ref" : "DBName" }, ";\\n",
          "GRANT ALL PRIVILEGES ON ", { "Ref" : "DBName" }, ".* TO \\"", { "Ref" : "DBUsername" }, "\\"@\\"localhost\\"\\n",
          "IDENTIFIED BY \\"", { "Ref" : "DBPassword" }, "\\";\\n",
          "FLUSH PRIVILEGES;\\n",
          "EXIT\\n",
          "EOF\\n",
          "sed -i \\"/Deny from All/d\\" /etc/httpd/conf.d/wordpress.conf\\n",
          "sed -i \\"s/Require local/Require all granted/\\" /etc/httpd/conf.d/wordpress.conf\\n",
          "sed --in-place --e s/database_name_here/", { "Ref" : "DBName" }, "/ --e s/username_here/", { "Ref" : "DBUsername" }, "/ --e s/password_here/", { "Ref" : "DBPassword" }, "/ /usr/share/wordpress/wp-config.php\\n",
          "systemctl restart httpd.service\\n"
        ]]}}
      }
    },
    "DataVolume" : {
      "Type" : "AWS::EC2::Volume",
      "Properties" : {
        "Size" : { "Ref" : "VolumeSize" },
        "AvailabilityZone" : { "Fn::GetAtt" : [ "WikiServer", "AvailabilityZone" ]},
        "Tags" : [{ "Key" : "Usage", "Value" : "Wiki Data Volume" }]
      }
    },
    "MountPoint" : {
      "Type" : "AWS::EC2::VolumeAttachment",
      "Properties" : {
        "InstanceId" : { "Ref" : "WikiServer" },
        "VolumeId"  : { "Ref" : "DataVolume" },
        "Device" : "/dev/vdc"
      }
    }
  },

  "Outputs" : {
    "WebsiteURL" : {
      "Value" : { "Fn::Join" : ["", ["http://", { "Fn::GetAtt" : [ "WikiServer", "PublicIp" ]}, "/wordpress"]] },
      "Description" : "URL for Wordpress wiki"
    },
    "InstanceIPAddress" : {
      "Value" : { "Ref" : "IPAddress" }
    }
  }
}
"""[1:]