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
    Contains the definition for the AWS AutoScalingGroup translator.
"""

from heat2arm import constants
from heat2arm.translators.base import BaseHeatARMTranslator


class AWSAutoScalingGroupARMTranslator(BaseHeatARMTranslator):
    """ AWSAutoScalingGroupARMTranslator is the translator for an
    AutoScalingGroup from CFN.

    It maps relatively cleanly into a set of Azure autoscaleSettings which is
    applied to an autoscaleGroup(the mapping of an AWS AvailabilityZone).
    However, some other components of the autoscaleSettings resource must be
    derived from a handful of different other AWS resources.
    """
    heat_resource_type = "AWS::AutoScaling::AutoScalingGroup"
    arm_resource_type = "Microsoft.Insights/autoscaleSettings"

    # def get_parameters(self):
    #    """ get_parameters returns a dict of the parameters required for the
    #    definition of the ARM resource.
    #    """
    #    pass

    def get_variables(self):
        """ get_variables returns the dict of all variables associated
        with the ARM definition of the resource.
        """
        variables = {
            "autoscaleSettingsName_%s" % self._name:
                "autoScaleSettings_%s" % self._name,
        }

        return variables

    # def get_dependencies(self):
    #    """ get_dependencies returns the list of dependencies of this resource
    #    """
    #    return []

    def get_resource_data(self):
        """ get_resource_data returns the dict of data associated with the
        definition of the resource in Azure.
        """
        res_data = [{
            "name": "[variables('autoscaleSettingsName_%s')]" % self._name,
            "apiVersion": constants.ARM_API_VERSION,
            "type": self.arm_resource_type,
            # NOTE: "dependsOn" necessary?
            "location": "[variables('location')]",
            "tags": {},    # NOTE
            "properties": {
                "name": "[variables('autoscaleSettingsName_%s')]" % self._name,
                "profiles": [self._get_profile()],
                "enabled": True,
                "targetResourceUri": self._get_target(),
            },
        }]

        return res_data

    def update_context(self):
        """ update_context adds all the necessary parameters, variables and
        resource data to the context required by this resource's translation.
        """
        pass

    def _get_capacity(self):
        """ _get_capacity is a helper method which returns the dictionary of
        capacity values for the profile for the new Azure autoscaleSettings.
        """
        maximum = int(self._heat_resource.properties.data["MaxSize"])
        minimum = int(self._heat_resource.properties.data["MinSize"])
        if not minimum > 0:
            # unlikely, but must be sure:
            raise Exception(
                "MinSize of AWS AutoScalingGroup '%s' is 0!" % self._name
            )

        # NOTE: default is the mean of the min and max by default:
        default = int((minimum + maximum) / 2)  # Python 3 futureproof'd
        if "DesiredCapacity" in self._heat_resource.properties.data:
            default = self._heat_resource.properties.data["DesiredCapacity"]

        return {
            "minimum": str(minimum),
            "default": str(default),
            "maximum": str(maximum),
        }

    def _get_recurrence(self):
        """ _get_recurrence is a helper method which returns the recurrence
        parameters for the profile for the new Azure autoscalingSettings.
        """
        return {}  # TODO (?)

    def _get_profile(self):
        """ _get_profile returns the single profile for the autoscaleSettings.
        """
        return {
            "name": "autoscaleSettingsProfile_%s" % self._name,
            "capacity": self._get_capacity(),
            "recurrence": self._get_recurrence()
        }

    def _get_target(self):
        """ _get_target returns the URI of the resource the autoscalingSettings
        should be applied to. The target is always an autoscalingSet.
        """
        if "AvailabilityZones" in self._heat_resource.properties.data:
            return ("[resourceId('Microsoft.Compute/availabilitySets', "
                    "variables('availabilitySetName_%s'))]" %
                    self._heat_resource.properties.data["AvailabilityZones"][0])
