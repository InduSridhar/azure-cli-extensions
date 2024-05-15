# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.testsdk import ScenarioTest
from azure.cli.testsdk.scenario_tests import AllowLargeResponse


class SupportScenarioTest(ScenarioTest):

    def cmd(self, command, checks=None, expect_failure=False):
        print("Running... {0}\n".format(command))
        rsp = super(SupportScenarioTest, self).cmd(command, checks=checks, expect_failure=expect_failure)

        try:
            rsp_json = rsp.get_output_in_json()
            print("Output... {0}\n".format(str(rsp_json)))
        except:
            pass

        return rsp

    def test_support_services(self):

        # List
        list_services_result = self.cmd('support services list').get_output_in_json()
        self.assertTrue(list_services_result is not None)
        self.assertTrue(len(list_services_result) > 100)
        self.assertTrue("type" in list_services_result[0])
        self.assertTrue(list_services_result[0]["type"] == "Microsoft.Support/services")
        self.assertTrue("name" in list_services_result[0])
        self.assertTrue("id" in list_services_result[0])

        # Show
        show_services_result = self.cmd('support services show --service-name ' +
                                        list_services_result[0]["name"]).get_output_in_json()
        self.assertTrue(show_services_result is not None)
        self.assertTrue("type" in show_services_result)
        self.assertTrue(show_services_result["type"] == "Microsoft.Support/services")
        self.assertTrue("name" in show_services_result)
        self.assertTrue("id" in show_services_result)
        self.assertTrue(show_services_result["id"] ==
                        "/providers/Microsoft.Support/services/" + show_services_result["name"])

        # List problem classifications
        list_problem_classifications_result = self.cmd('az support services problem-classifications list --service-name ' +
                                                       list_services_result[0]["name"]).get_output_in_json()
        self.assertTrue(list_problem_classifications_result is not None)
        self.assertTrue(len(list_problem_classifications_result) > 0)
        self.assertTrue("type" in list_problem_classifications_result[0])
        self.assertTrue(list_problem_classifications_result[0]["type"] ==
                        "Microsoft.Support/problemClassifications")
        self.assertTrue("name" in list_problem_classifications_result[0])
        self.assertTrue("id" in list_problem_classifications_result[0])

        # Show problem classification
        show_problem_classifications_result = self.cmd('az support services problem-classifications show --service-name ' +
                                                       list_services_result[0]["name"] + ' --problem-classification-name ' +
                                                       list_problem_classifications_result[0]["name"]).get_output_in_json()
        self.assertTrue(show_problem_classifications_result is not None)
        self.assertTrue("type" in show_problem_classifications_result)
        self.assertTrue(show_problem_classifications_result["type"] ==
                        "Microsoft.Support/problemClassifications")
        self.assertTrue("name" in show_problem_classifications_result)
        self.assertTrue("id" in show_problem_classifications_result)
        self.assertTrue(show_problem_classifications_result["id"] ==
                        "/providers/Microsoft.Support/services/" + list_services_result[0]["name"] +
                        "/problemClassifications/" + list_problem_classifications_result[0]["name"])

    def test_support_tickets_create_validations(self):
        test_ticket_name = self.create_random_name(prefix='test_ticket_from_cli_', length=30)
        service_name = "06bfd9d3-516b-d5c6-5802-169c800dec89"
        problem_classification_name = "e12e3d1d-7fa0-af33-c6d0-3c50df9658a3"
        invalid_arm_resource_id = "/subscriptions/1c4eecc5-46a8-4b7f-9a0a-fa0ba47240cd"
        invalid_arm_resource_id += "/resourceGroups/test/providers/Microsoft.Compute/virtualMachines/testserver"
        base_cmd = self._build_base_support_tickets_create_command(test_ticket_name)

        # Failure scenario - invalid prefix problem classifications
        cmd = str(base_cmd)
        cmd += "--problem-classification '/providers/Microsoft.Support/services/0/{0}/".format(service_name)
        cmd += "problemClassifications/{0}' ".format(problem_classification_name)
        rsp = self.cmd(cmd, expect_failure=True)
        self._validate_failure_rsp(rsp, 1)

        # Failure scenario - invalid guid problem classifications
        cmd = str(base_cmd)
        cmd += "--problem-classification '/providers/Microsoft.Support/services/{0}/".format(service_name)
        cmd += "problemClassifications/{0}0' ".format(problem_classification_name)
        rsp = self.cmd(cmd, expect_failure=True)
        self._validate_failure_rsp(rsp, 1)

        # Failure scenario - invalid resource id
        cmd = str(base_cmd)
        cmd += "--problem-classification '/providers/Microsoft.Support/services/{0}/".format(service_name)
        cmd = cmd.replace(service_name, "cddd3eb5-1830-b494-44fd-782f691479dc")
        cmd += "problemClassifications/{0}' ".format("ef8b3865-0c5a-247b-dcaa-d70fd7611a3c")
        cmd += "--technical-resource '{0}' ".format(invalid_arm_resource_id)
        rsp = self.cmd(cmd, expect_failure=True)
        self._validate_failure_rsp(rsp, 1)

        # Failure scenario - invalid ticket name
        cmd = str(base_cmd)
        cmd = cmd.replace(test_ticket_name, "12345")
        cmd += "--problem-classification '/providers/Microsoft.Support/services/{0}/".format(service_name)
        cmd += "problemClassifications/{0}' ".format(problem_classification_name)
        rsp = self.cmd(cmd, expect_failure=True)
        self._validate_failure_rsp(rsp, 1)

    @AllowLargeResponse(size_kb=9999)
    def test_support_tickets(self):
        random_guid = "12345678-1234-1234-1234-123412341234"
        test_ticket_name = self.create_random_name(prefix='test_ticket_from_cli_', length=30)
        test_communication_name = self.create_random_name(prefix='test_communication_from_cli_', length=40)

        # Create billing
        base_cmd = self._build_base_support_tickets_create_command(test_ticket_name)
        billing_cmd = self._build_support_tickets_create_billing_cmd()
        cmd = "{0} {1}".format(base_cmd, billing_cmd)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_base_support_tickets_create_command(rsp, test_ticket_name)

        # Create communication 1 - invalid communication name
        cmd = self._build_support_tickets_communications_create_cmd(test_ticket_name, random_guid)
        rsp = self.cmd(cmd, expect_failure=True)
        self._validate_failure_rsp(rsp, 1)

        # Create communication 2
        cmd = self._build_support_tickets_communications_create_cmd(test_ticket_name, test_communication_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_communications_create_cmd(rsp, test_ticket_name, test_communication_name)

        # List communications
        cmd = self._build_support_tickets_communications_list_cmd(test_ticket_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_communications_list_cmd(rsp, test_ticket_name, test_communication_name)

        # Show communication
        cmd = self._build_support_tickets_communications_show_cmd(test_ticket_name, test_communication_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_communications_show_cmd(rsp, test_ticket_name, test_communication_name)
        
        # List tickets
        cmd = self._build_support_tickets_list_cmd()
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_list_cmd(rsp, test_ticket_name)

        # Update severity/contact 1
        cmd = self._build_support_tickets_update_cmd1(test_ticket_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_update_cmd1(rsp)

        # Update severity/contact 2
        cmd = self._build_support_tickets_update_cmd2(test_ticket_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_update_cmd2(rsp)

        # Update diagnostic consent
        cmd = self._build_support_tickets_update_cmd3(test_ticket_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_update_cmd3(rsp)

        # Update status
        cmd = self._build_support_tickets_update_cmd5(test_ticket_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_update_cmd5(rsp)

        # Show
        cmd = self._build_support_tickets_show_cmd(test_ticket_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_support_tickets_show_cmd(rsp, test_ticket_name)

    def test_chat_transcript(self):
        test_ticket_name = "58cf91d7-27a54e37-7ee57473-c9c9-4350-b0e1-f7aa2479108d"
        test_chat_transcript_name = "e3bc592b-ba39-49d3-8853-16e33023b22b"

        # List Chat Transcript
        cmd = self._build_chat_transcript_list_cmd(test_ticket_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_chat_transcript_list_cmd(rsp, test_chat_transcript_name)

        # Show Chat Transcript
        cmd = self._build_chat_transcript_show_cmd(test_ticket_name, test_chat_transcript_name)
        rsp = self.cmd(cmd).get_output_in_json()
        self._validate_chat_transcript_show_cmd(rsp, test_chat_transcript_name)

    def test_support_file_attachment_in_subscription(self):
        # this tests the scenario where the user inputs the subscription that is different from the account subscription
        # CLI subscription scenario
        # Retrieve subscription ID
        subscription = get_subscription_id(self.cli_ctx)

        # Create File workspace
        file_workspace_name_cli = self.create_random_name(prefix='in_sub_cli_', length=20)
        self._validate_create_file_workspace_cli_in_subscription(file_workspace_name_cli, subscription)

        # Show File workspace
        self._validate_show_file_workspace_cli_in_subscription(file_workspace_name_cli, subscription)

        # Upload File
        file_name = "testFile.txt"
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        file_path = file_path.replace('\\', '\\\\')
        self._validate_upload_file_cli_in_subscription(file_workspace_name_cli, file_path, subscription)

        # List File
        self._validate_list_file_cli_in_subscription(file_workspace_name_cli, subscription)

        # Show File
        self._validate_show_file_cli_in_subscription(file_workspace_name_cli, file_name, subscription)

        # this tests the scenario where the user does not input the subscription since it is the same as the account subscription
        # In Account subscription scenario

        # Create File workspace
        file_workspace_name_for_account = self.create_random_name(prefix='in_sub_account_', length=20)

        self._validate_create_file_workspace_account_in_subscription(file_workspace_name_for_account)

        # Show File workspace
        self._validate_show_file_workspace_account_in_subscription(file_workspace_name_for_account)

        # Upload File
        self._validate_upload_file_account_in_subscription(file_workspace_name_for_account, file_path)

        # List File
        self._validate_list_file_account_in_subscription(file_workspace_name_for_account)

        # Show File
        self._validate_show_file_account_in_subscription(file_workspace_name_for_account, file_name)

    def _build_base_support_tickets_create_command(self, test_ticket_name):
        test_ticket_title = "test ticket from python cli test. Do not assign and close after a day."
        cmd = "support in-subscription tickets create --debug "
        cmd += "--description '{0}' ".format(test_ticket_title)
        cmd += "--severity 'minimal' "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--title '{0}' ".format(test_ticket_title)
        cmd += "--contact-country 'USA' "
        cmd += "--contact-email 'azengcase@microsoft.com' "
        cmd += "--contact-first-name 'Foo' "
        cmd += "--contact-language 'en-us' "
        cmd += "--contact-last-name 'Bar' "
        cmd += "--contact-method 'email' "
        cmd += "--contact-timezone 'Pacific Standard Time' "
        cmd += "--advanced-diagnostic-consent 'No' "

        return cmd

    def _build_support_tickets_create_billing_cmd(self):
        service_name = "517f2da6-78fd-0498-4e22-ad26996b1dfc"
        problem_classification_name = "44114011-6a66-e902-c00f-e419b6b4509f"
        cmd = "--problem-classification '/providers/Microsoft.Support/services/{0}/".format(service_name)
        cmd += "problemClassifications/{0}' ".format(problem_classification_name)

        return cmd

    def _validate_base_support_tickets_create_command(self, rsp, test_ticket_name):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/supportTickets")
        self.assertTrue("name" in rsp)
        self.assertTrue(rsp["name"] == test_ticket_name)
        self.assertTrue("require24X7Response" in rsp)
        self.assertTrue(rsp["require24X7Response"] is False)

    def _build_support_tickets_communications_create_cmd(self, test_ticket_name, test_communication_name):
        cmd = "support in-subscription communication create --debug "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--communication-name '{0}' ".format(test_communication_name)
        cmd += "--communication-sender 'rushar@microsoft.com' "
        cmd += "--communication-subject 'test subject for communication posted from azure python cli' "
        cmd += "--communication-body  'test body for communication posted from azure python cli' "

        return cmd

    def _validate_support_tickets_communications_create_cmd(self, rsp, test_ticket_name, test_communication_name):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/communications")
        self.assertTrue("name" in rsp)
        self.assertTrue(rsp["name"] == test_communication_name)

    def _build_support_tickets_communications_list_cmd(self, test_ticket_name):
        cmd = "support in-subscription communication list "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)

        return cmd

    def _validate_support_tickets_communications_list_cmd(self, rsp, test_ticket_name, test_communication_name):
        self.assertTrue(rsp is not None)
        self.assertTrue(len(rsp) >= 1)
        self.assertTrue("type" in rsp[0])
        self.assertTrue(rsp[0]["type"] == "Microsoft.Support/communications")
        self.assertTrue("name" in rsp[0])

        communication_returned = False
        for communication in rsp:
            if communication["name"] == test_communication_name:
                communication_returned = True
                break

        self.assertTrue(communication_returned is True)

    def _build_support_tickets_communications_show_cmd(self, test_ticket_name, test_communication_name):
        cmd = "support in-subscription communication show "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--communication-name '{0}' ".format(test_communication_name)

        return cmd

    def _validate_support_tickets_communications_show_cmd(self, rsp, test_ticket_name, test_communication_name):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/communications")
        self.assertTrue("name" in rsp)
        self.assertTrue(rsp["name"] == test_communication_name)

    def _build_support_tickets_list_cmd(self):
        cmd = "support in-subscription tickets list --max-items 3 "
        cmd += "--filter \"status eq 'Open'\" "

        return cmd

    def _validate_support_tickets_list_cmd(self, rsp, test_ticket_name):
        self.assertTrue(rsp is not None)
        self.assertTrue(len(rsp) >= 1)
        self.assertTrue("type" in rsp[0])
        self.assertTrue(rsp[0]["type"] == "Microsoft.Support/supportTickets")
        self.assertTrue("name" in rsp[0])

        ticket_returned = False
        for ticket in rsp:
            if ticket["name"] == test_ticket_name:
                ticket_returned = True
                break

        self.assertTrue(ticket_returned is True)

    def _build_support_tickets_update_cmd1(self, test_ticket_name):
        cmd = "support in-subscription tickets update "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--severity 'moderate' "
        cmd += "--contact-method 'phone' "
        cmd += "--contact-phone-number '123-456-7890' "

        return cmd

    def _validate_support_tickets_update_cmd1(self, rsp):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/supportTickets")
        self.assertTrue("severity" in rsp)
        self.assertTrue("Moderate" == rsp["severity"])
        self.assertTrue("contactDetails" in rsp)
        self.assertTrue("123-456-7890" == rsp["contactDetails"]["phoneNumber"])
        self.assertTrue("Phone" == rsp["contactDetails"]["preferredContactMethod"])

    def _build_support_tickets_update_cmd2(self, test_ticket_name):
        cmd = "support in-subscription tickets update "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--severity 'minimal' "
        cmd += "--contact-method 'email' "

        return cmd

    def _validate_support_tickets_update_cmd2(self, rsp):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/supportTickets")
        self.assertTrue("severity" in rsp)
        self.assertTrue("Minimal" == rsp["severity"])
        self.assertTrue("contactDetails" in rsp)
        self.assertTrue("Email" == rsp["contactDetails"]["preferredContactMethod"])
        
    def _build_support_tickets_update_cmd3(self, test_ticket_name):
        cmd = "support in-subscription tickets update "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--advanced-diagnostic-consent 'Yes'"
        
        return cmd
        
    def _validate_support_tickets_update_cmd3(self, rsp):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/supportTickets")
        self.assertTrue("advancedDiagnosticConsent" in rsp)
        self.assertTrue("Yes" == rsp["advancedDiagnosticConsent"])

    def _build_support_tickets_update_cmd5(self, test_ticket_name):
        cmd = "support in-subscription tickets update "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--status 'closed' "

        return cmd

    def _validate_support_tickets_update_cmd5(self, rsp):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/supportTickets")
        self.assertTrue("status" in rsp)
        self.assertTrue("closed" == rsp["status"])

    def _build_support_tickets_show_cmd(self, test_ticket_name):
        cmd = "support in-subscription tickets show "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)

        return cmd

    def _validate_support_tickets_show_cmd(self, rsp, test_ticket_name):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/supportTickets")
        self.assertTrue("name" in rsp)
        self.assertTrue(rsp["name"] == test_ticket_name)

    def _validate_failure_rsp(self, rsp, exit_code):
        self.assertTrue(rsp is not None)
        self.assertTrue(rsp.exit_code is not None)
        self.assertTrue(rsp.exit_code == exit_code)

    def _build_chat_transcript_list_cmd(self, test_ticket_name):
        cmd = "support in-subscription chat-transcript list "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)

        return cmd

    def _validate_chat_transcript_list_cmd(self, rsp, test_chat_transcript_name):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp[0])
        self.assertTrue(rsp[0]["type"] == "Microsoft.Support/chatTranscripts")
        self.assertTrue("name" in rsp[0])
        self.assertTrue(rsp[0]["name"] == test_chat_transcript_name)

    def _build_chat_transcript_show_cmd(self, test_ticket_name, test_chat_transcript_name):
        cmd = "support in-subscription chat-transcript show "
        cmd += "--ticket-name '{0}' ".format(test_ticket_name)
        cmd += "--chat-transcript-name '{0}' ".format(test_chat_transcript_name)

        return cmd

    def _validate_chat_transcript_show_cmd(self, rsp, test_chat_transcript_name):
        self.assertTrue(rsp is not None)
        self.assertTrue("type" in rsp)
        self.assertTrue(rsp["type"] == "Microsoft.Support/chatTranscripts")
        self.assertTrue("name" in rsp)
        self.assertTrue(rsp["name"] == test_chat_transcript_name)

    def _validate_create_file_workspace_cli_in_subscription(self, file_workspace_name, subscription):
        create_file_workspace_result = self.cmd('support in-subscription file-workspace create --file-workspace-name ' + file_workspace_name + ' --subscription ' + subscription).get_output_in_json()
        self.assertTrue(create_file_workspace_result is not None)
        self.assertTrue("type" in create_file_workspace_result)
        self.assertTrue(create_file_workspace_result["type"] == "Microsoft.Support/fileWorkspaces")
        self.assertTrue("name" in create_file_workspace_result)
        self.assertTrue(create_file_workspace_result["name"] == file_workspace_name)
        self.assertTrue("id" in create_file_workspace_result)
        self.assertTrue(("/subscriptions/"+subscription+"/providers/Microsoft.Support/fileWorkspaces/" + file_workspace_name) == create_file_workspace_result["id"])
        self.assertTrue("createdOn" in create_file_workspace_result)
        self.assertTrue("expirationTime" in create_file_workspace_result)

    def _validate_show_file_workspace_cli_in_subscription(self, file_workspace_name, subscription):
        show_file_workspace_result = self.cmd('support in-subscription file-workspace show --file-workspace-name ' + file_workspace_name + ' --subscription ' + subscription).get_output_in_json()
        self.assertTrue(show_file_workspace_result is not None)
        self.assertTrue("type" in show_file_workspace_result)
        self.assertTrue(show_file_workspace_result["type"] == "Microsoft.Support/fileWorkspaces")
        self.assertTrue("name" in show_file_workspace_result)
        self.assertTrue(show_file_workspace_result["name"] == file_workspace_name)
        self.assertTrue("id" in show_file_workspace_result)
        self.assertTrue(("/subscriptions/"+subscription+"/providers/Microsoft.Support/fileWorkspaces/" + file_workspace_name) == show_file_workspace_result["id"])
        self.assertTrue("createdOn" in show_file_workspace_result)
        self.assertTrue("expirationTime" in show_file_workspace_result)

    def _validate_upload_file_cli_in_subscription(self, file_workspace_name, file_path, subscription):
        upload_file_result = self.cmd('support in-subscription file upload --file-workspace-name ' + file_workspace_name + ' --file-path ' + file_path + ' --subscription ' + subscription)

    def _validate_list_file_cli_in_subscription(self, file_workspace_name, subscription):
        list_file_attachment_result = self.cmd('support in-subscription file list --file-workspace-name ' + file_workspace_name + ' --subscription ' + subscription).get_output_in_json()
        self.assertTrue(list_file_attachment_result is not None)
        self.assertTrue(len(list_file_attachment_result) >= 1)
        self.assertTrue("type" in list_file_attachment_result[0])
        self.assertTrue(list_file_attachment_result[0]["type"] == "Microsoft.Support/files")
        self.assertTrue("name" in list_file_attachment_result[0])
        self.assertTrue("id" in list_file_attachment_result[0])
        self.assertTrue("chunkSize" in list_file_attachment_result[0])
        self.assertTrue("createdOn" in list_file_attachment_result[0])
        self.assertTrue("fileSize" in list_file_attachment_result[0])
        self.assertTrue("numberOfChunks" in list_file_attachment_result[0])
        self.assertTrue(list_file_attachment_result[0]["chunkSize"] <= 1024 * 1024 * 2.5)
        self.assertTrue(list_file_attachment_result[0]["fileSize"] <= 1024 * 1024 * 5.0)
        self.assertTrue(list_file_attachment_result[0]["numberOfChunks"] <= 2.0)

    def _validate_show_file_cli_in_subscription(self, file_workspace_name, file_name, subscription):
        show_file_result = self.cmd('support in-subscription file show --file-workspace-name ' + file_workspace_name + ' --file-name ' +
        file_name + ' --subscription ' + subscription).get_output_in_json()
        self.assertTrue(show_file_result is not None)
        self.assertTrue("type" in show_file_result)
        self.assertTrue(show_file_result["type"] == "Microsoft.Support/files")
        self.assertTrue("name" in show_file_result)
        self.assertTrue("id" in show_file_result)
        self.assertTrue("chunkSize" in show_file_result)
        self.assertTrue("createdOn" in show_file_result)
        self.assertTrue("fileSize" in show_file_result)
        self.assertTrue("numberOfChunks" in show_file_result)
        self.assertTrue(show_file_result["chunkSize"] <= 1024 * 1024 * 2.5)
        self.assertTrue(show_file_result["fileSize"] <= 1024 * 1024 * 5.0)
        self.assertTrue(show_file_result["numberOfChunks"] <= 2.0)

    def _validate_create_file_workspace_account_in_subscription(self, file_workspace_name):
        create_file_workspace_result = self.cmd('support in-subscription file-workspace create --file-workspace-name ' + file_workspace_name).get_output_in_json()
        self.assertTrue(create_file_workspace_result is not None)
        self.assertTrue("type" in create_file_workspace_result)
        self.assertTrue(create_file_workspace_result["type"] == "Microsoft.Support/fileWorkspaces")
        self.assertTrue("name" in create_file_workspace_result)
        self.assertTrue(create_file_workspace_result["name"] == file_workspace_name)
        self.assertTrue("id" in create_file_workspace_result)
        self.assertTrue(("/providers/Microsoft.Support/fileWorkspaces/" + file_workspace_name) in create_file_workspace_result["id"])
        self.assertTrue("createdOn" in create_file_workspace_result)
        self.assertTrue("expirationTime" in create_file_workspace_result)

    def _validate_show_file_workspace_account_in_subscription(self, file_workspace_name):
        show_file_workspace_result = self.cmd('support in-subscription file-workspace show --file-workspace-name ' + file_workspace_name).get_output_in_json()
        self.assertTrue(show_file_workspace_result is not None)
        self.assertTrue("type" in show_file_workspace_result)
        self.assertTrue(show_file_workspace_result["type"] == "Microsoft.Support/fileWorkspaces")
        self.assertTrue("name" in show_file_workspace_result)
        self.assertTrue(show_file_workspace_result["name"] == file_workspace_name)
        self.assertTrue("id" in show_file_workspace_result)
        self.assertTrue(("/providers/Microsoft.Support/fileWorkspaces/" + file_workspace_name) in show_file_workspace_result["id"])
        self.assertTrue("createdOn" in show_file_workspace_result)
        self.assertTrue("expirationTime" in show_file_workspace_result)

    def _validate_upload_file_account_in_subscription(self, file_workspace_name, file_path):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testFile.txt")
        file_path = file_path.replace('\\','\\\\')
        upload_file_result = self.cmd('support in-subscription file upload --file-workspace-name ' + file_workspace_name + ' --file-path ' + file_path)
     
    def _validate_list_file_account_in_subscription(self, file_workspace_name):
        list_file_attachment_result = self.cmd('support in-subscription file list --file-workspace-name ' + file_workspace_name).get_output_in_json()
        self.assertTrue(list_file_attachment_result is not None)
        self.assertTrue(len(list_file_attachment_result) >= 1)
        self.assertTrue("type" in list_file_attachment_result[0])
        self.assertTrue(list_file_attachment_result[0]["type"] == "Microsoft.Support/files")
        self.assertTrue("name" in list_file_attachment_result[0])
        self.assertTrue("id" in list_file_attachment_result[0])
        self.assertTrue("chunkSize" in list_file_attachment_result[0])
        self.assertTrue("createdOn" in list_file_attachment_result[0])
        self.assertTrue("fileSize" in list_file_attachment_result[0])
        self.assertTrue("numberOfChunks" in list_file_attachment_result[0])
        self.assertTrue(list_file_attachment_result[0]["chunkSize"] <= 1024 * 1024 * 2.5)
        self.assertTrue(list_file_attachment_result[0]["fileSize"] <= 1024 * 1024 * 5.0)
        self.assertTrue(list_file_attachment_result[0]["numberOfChunks"] <= 2.0)

    def _validate_show_file_account_in_subscription(self, file_workspace_name, file_name):
        show_file_result = self.cmd('support in-subscription file show --file-workspace-name ' + file_workspace_name + ' --file-name ' +
        file_name).get_output_in_json()
        self.assertTrue(show_file_result is not None)
        self.assertTrue("type" in show_file_result)
        self.assertTrue(show_file_result["type"] == "Microsoft.Support/files")
        self.assertTrue("name" in show_file_result)
        self.assertTrue("id" in show_file_result)
        self.assertTrue("chunkSize" in show_file_result)
        self.assertTrue("createdOn" in show_file_result)
        self.assertTrue("fileSize" in show_file_result)
        self.assertTrue("numberOfChunks" in show_file_result)
        self.assertTrue(show_file_result["chunkSize"] <= 1024 * 1024 * 2.5)
        self.assertTrue(show_file_result["fileSize"] <= 1024 * 1024 * 5.0)
        self.assertTrue(show_file_result["numberOfChunks"] <= 2.0)