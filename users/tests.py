# # views.py - Add this new view to orchestrate the complete flow

# import asyncio
# import time
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import logging

# logger = logging.getLogger(__name__)

# class CompleteSIPFlowView(APIView):
#     """
#     Orchestrates the complete SIP creation flow with a single API call
#     """
    
#     def post(self, request, *args, **kwargs):
#         preferred_type = request.data.get('preferred_type', 'SIP')
        
#         try:
#             # Step 1: Search
#             search_result = self._execute_search()
#             if not search_result['success']:
#                 return Response(search_result, status=status.HTTP_400_BAD_REQUEST)
            
#             transaction_id = search_result['transaction_id']
            
#             # Step 2: Wait for on_search callback (with timeout)
#             on_search_data = self._wait_for_on_search(transaction_id)
#             if not on_search_data:
#                 return Response({
#                     'success': False, 
#                     'error': 'Timeout waiting for search results'
#                 }, status=status.HTTP_408_REQUEST_TIMEOUT)
            
#             # Step 3: Select SIP
#             select_result = self._execute_select(
#                 transaction_id, 
#                 on_search_data['bpp_id'], 
#                 on_search_data['bpp_uri'], 
#                 preferred_type
#             )
#             if not select_result['success']:
#                 return Response(select_result, status=status.HTTP_400_BAD_REQUEST)
            
#             # Step 4: Wait for on_select callback
#             on_select_data = self._wait_for_on_select(transaction_id)
#             if not on_select_data:
#                 return Response({
#                     'success': False, 
#                     'error': 'Timeout waiting for select confirmation'
#                 }, status=status.HTTP_408_REQUEST_TIMEOUT)
            
#             # Step 5: Submit Form (if required)
#             form_result = self._execute_form_submission(
#                 transaction_id, 
#                 on_select_data['bpp_id'], 
#                 on_select_data['bpp_uri']
#             )
#             if not form_result['success']:
#                 return Response(form_result, status=status.HTTP_400_BAD_REQUEST)
            
#             # Step 6: Initialize
#             init_result = self._execute_init(
#                 transaction_id, 
#                 on_select_data['bpp_id'], 
#                 on_select_data['bpp_uri'],
#                 form_result['message_id']
#             )
#             if not init_result['success']:
#                 return Response(init_result, status=status.HTTP_400_BAD_REQUEST)
            
#             # Step 7: Wait for on_init callback
#             on_init_data = self._wait_for_on_init(transaction_id)
#             if not on_init_data:
#                 return Response({
#                     'success': False, 
#                     'error': 'Timeout waiting for init confirmation'
#                 }, status=status.HTTP_408_REQUEST_TIMEOUT)
            
#             # Step 8: Confirm SIP
#             confirm_result = self._execute_confirm(
#                 transaction_id, 
#                 on_init_data['bpp_id'], 
#                 on_init_data['bpp_uri'],
#                 on_init_data['message_id']
#             )
#             if not confirm_result['success']:
#                 return Response(confirm_result, status=status.HTTP_400_BAD_REQUEST)
            
#             # Step 9: Wait for final on_confirm callback
#             on_confirm_data = self._wait_for_on_confirm(transaction_id)
#             if not on_confirm_data:
#                 return Response({
#                     'success': False, 
#                     'error': 'Timeout waiting for final confirmation'
#                 }, status=status.HTTP_408_REQUEST_TIMEOUT)
            
#             return Response({
#                 'success': True,
#                 'message': 'SIP created successfully',
#                 'transaction_id': transaction_id,
#                 'order_details': on_confirm_data.get('order_details'),
#                 'flow_summary': {
#                     'search_completed': True,
#                     'select_completed': True,
#                     'form_submitted': True,
#                     'init_completed': True,
#                     'confirm_completed': True
#                 }
#             }, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             logger.error(f"Complete SIP flow failed: {str(e)}", exc_info=True)
#             return Response({
#                 'success': False,
#                 'error': f'Flow execution failed: {str(e)}'
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     def _execute_search(self):
#         """Execute the search step"""
#         try:
#             transaction_id = str(uuid.uuid4())
#             message_id = str(uuid.uuid4())
#             timestamp = datetime.utcnow().isoformat(sep="T", timespec="milliseconds") + "Z"
            
#             payload = {
#                 "context": {
#                     "location": {"country": {"code": "IND"}, "city": {"code": "*"}},
#                     "domain": "ONDC:FIS14",
#                     "timestamp": timestamp,
#                     "bap_id": "investment.preprod.vyable.in",
#                     "bap_uri": "https://investment.preprod.vyable.in/ondc",
#                     "transaction_id": transaction_id,
#                     "message_id": message_id,
#                     "version": "2.0.0",
#                     "ttl": "PT10M",
#                     "action": "search"
#                 },
#                 "message": {
#                     "intent": {
#                         "category": {"descriptor": {"code": "MUTUAL_FUNDS"}},
#                         "fulfillment": {
#                             "agent": {
#                                 "organization": {
#                                     "creds": [{"id": "ARN-125784", "type": "ARN"}]
#                                 }
#                             }
#                         },
#                         "tags": [{
#                             "display": False,
#                             "descriptor": {"name": "BAP Terms of Engagement", "code": "BAP_TERMS"},
#                             "list": [
#                                 {
#                                     "descriptor": {"name": "Static Terms (Transaction Level)", "code": "STATIC_TERMS"},
#                                     "value": "https://buyerapp.com/legal/ondc:fis14/static_terms?v=0.1"
#                                 },
#                                 {
#                                     "descriptor": {"name": "Offline Contract", "code": "OFFLINE_CONTRACT"},
#                                     "value": "true"
#                                 }
#                             ]
#                         }]
#                     }
#                 }
#             }
            
#             # Store transaction
#             transaction, _ = Transaction.objects.get_or_create(transaction_id=transaction_id)
#             Message.objects.create(
#                 transaction=transaction,
#                 message_id=message_id,
#                 action="search",
#                 timestamp=parse_datetime(timestamp),
#                 payload=payload
#             )
            
#             # Send request
#             request_body_str = json.dumps(payload, separators=(',', ':'))
#             auth_header = create_authorisation_header(request_body=request_body_str)
            
#             headers = {
#                 "Content-Type": "application/json",
#                 "Authorization": auth_header,
#                 "X-Gateway-Authorization": os.getenv("SIGNED_UNIQUE_REQ_ID", ""),
#                 "X-Gateway-Subscriber-Id": os.getenv("SUBSCRIBER_ID")
#             }
            
#             response = requests.post("https://preprod.gateway.ondc.org/search", 
#                                    data=request_body_str, headers=headers)
            
#             if response.status_code == 200:
#                 return {
#                     'success': True,
#                     'transaction_id': transaction_id,
#                     'message_id': message_id
#                 }
#             else:
#                 return {
#                     'success': False,
#                     'error': f'Search request failed with status {response.status_code}'
#                 }
                
#         except Exception as e:
#             return {'success': False, 'error': str(e)}
    
#     def _wait_for_on_search(self, transaction_id, timeout=30):
#         """Wait for on_search callback with timeout"""
#         start_time = time.time()
#         while time.time() - start_time < timeout:
#             try:
#                 transaction = Transaction.objects.get(transaction_id=transaction_id)
#                 search_entry = FullOnSearch.objects.filter(transaction=transaction).first()
#                 if search_entry:
#                     payload = search_entry.payload
#                     return {
#                         'bpp_id': payload['context']['bpp_id'],
#                         'bpp_uri': payload['context']['bpp_uri'],
#                         'payload': payload
#                     }
#             except:
#                 pass
#             time.sleep(2)  # Wait 2 seconds before checking again
#         return None
    
#     def _execute_select(self, transaction_id, bpp_id, bpp_uri, preferred_type):
#         """Execute the select step"""
#         try:
#             obj = FullOnSearch.objects.get(
#                 payload__context__bpp_id=bpp_id,
#                 payload__context__bpp_uri=bpp_uri,
#                 transaction__transaction_id=transaction_id
#             )
            
#             message_id = str(uuid.uuid4())
#             timestamp = datetime.utcnow().isoformat(sep="T", timespec="milliseconds") + "Z"
            
#             provider = obj.payload["message"]["catalog"]["providers"][0]
#             matching_fulfillment = next(
#                 (f for f in provider["fulfillments"] if f.get("type") == preferred_type), None
#             )
            
#             if not matching_fulfillment:
#                 return {'success': False, 'error': f'No fulfillment with type {preferred_type} found'}
            
#             # Build select payload (similar to your existing SIPCreationView)
#             payload = {
#                 "context": {
#                     "location": {"country": {"code": "IND"}, "city": {"code": "*"}},
#                     "domain": "ONDC:FIS14",
#                     "timestamp": timestamp,
#                     "bap_id": "investment.preprod.vyable.in",
#                     "bap_uri": "https://investment.preprod.vyable.in/ondc",
#                     "transaction_id": transaction_id,
#                     "message_id": message_id,
#                     "version": "2.0.0",
#                     "ttl": "PT10M",
#                     "bpp_id": bpp_id,
#                     "bpp_uri": bpp_uri,
#                     "action": "select"
#                 },
#                 "message": {
#                     "order": {
#                         "provider": {"id": provider['id']},
#                         "items": [{
#                             "id": provider['items'][0]['id'],
#                             "quantity": {
#                                 "selected": {
#                                     "measure": {"value": "3000", "unit": "INR"}
#                                 }
#                             }
#                         }],
#                         "fulfillments": [{
#                             "id": matching_fulfillment['id'],
#                             "type": matching_fulfillment['type'],
#                             "customer": {"person": {"id": "pan:arrpp7771n"}},
#                             "agent": {
#                                 "person": {"id": "euin:E52432"},
#                                 "organization": {
#                                     "creds": [
#                                         {"id": "ARN-124567", "type": "ARN"},
#                                         {"id": "ARN-123456", "type": "SUB_BROKER_ARN"}
#                                     ]
#                                 }
#                             },
#                             "stops": [{
#                                 "time": {
#                                     "schedule": {
#                                         "frequency": matching_fulfillment["tags"][0]["list"][0]["value"]
#                                     }
#                                 }
#                             }]
#                         }],
#                         "tags": [{
#                             "display": False,
#                             "descriptor": {"name": "BAP Terms of Engagement", "code": "BAP_TERMS"},
#                             "list": [
#                                 {
#                                     "descriptor": {"name": "Static Terms (Transaction Level)", "code": "STATIC_TERMS"},
#                                     "value": "https://buyerapp.com/legal/ondc:fis14/static_terms?v=0.1"
#                                 },
#                                 {
#                                     "descriptor": {"name": "Offline Contract", "code": "OFFLINE_CONTRACT"},
#                                     "value": "true"
#                                 }
#                             ]
#                         }]
#                     }
#                 }
#             }
            
#             # Store and send
#             transaction = Transaction.objects.get(transaction_id=transaction_id)
#             Message.objects.create(
#                 transaction=transaction,
#                 message_id=message_id,
#                 action="select",
#                 timestamp=parse_datetime(timestamp),
#                 payload=payload
#             )
            
#             request_body_str = json.dumps(payload, separators=(',', ':'))
#             auth_header = create_authorisation_header(request_body=request_body_str)
            
#             headers = {
#                 "Content-Type": "application/json",
#                 "Authorization": auth_header,
#                 "X-Gateway-Authorization": os.getenv("SIGNED_UNIQUE_REQ_ID", ""),
#                 "X-Gateway-Subscriber-Id": os.getenv("SUBSCRIBER_ID")
#             }
            
#             response = requests.post(f"{bpp_uri}/select", data=request_body_str, headers=headers)
            
#             if response.status_code == 200:
#                 return {'success': True, 'message_id': message_id}
#             else:
#                 return {'success': False, 'error': f'Select request failed with status {response.status_code}'}
                
#         except Exception as e:
#             return {'success': False, 'error': str(e)}
    
#     def _wait_for_on_select(self, transaction_id, timeout=30):
#         """Wait for on_select callback"""
#         start_time = time.time()
#         while time.time() - start_time < timeout:
#             try:
#                 transaction = Transaction.objects.get(transaction_id=transaction_id)
#                 select_entry = SelectSIP.objects.filter(transaction=transaction).first()
#                 if select_entry:
#                     payload = select_entry.payload
#                     return {
#                         'bpp_id': payload['context']['bpp_id'],
#                         'bpp_uri': payload['context']['bpp_uri'],
#                         'message_id': payload['context']['message_id'],
#                         'payload': payload
#                     }
#             except:
#                 pass
#             time.sleep(2)
#         return None
    
#     def _execute_form_submission(self, transaction_id, bpp_id, bpp_uri):
#         """Execute form submission step"""
#         try:
#             obj = SelectSIP.objects.get(
#                 payload__context__bpp_id=bpp_id,
#                 payload__context__bpp_uri=bpp_uri,
#                 transaction__transaction_id=transaction_id
#             )
            
#             message_id = str(uuid.uuid4())
#             timestamp = datetime.utcnow().isoformat(sep="T", timespec="milliseconds") + "Z"
            
#             # Extract form URL
#             xinput = obj.payload["message"]["order"]["xinput"]
#             url = xinput["form"]["url"]
            
#             # Submit KYC data
#             user_kyc_data = {
#                 "pan": "ABCDE1234F",
#                 "dob": "1990-01-01",
#                 "email": "user@example.com",
#                 "name": "Ravi Kumar",
#                 "gender": "Male",
#                 "marital_status": "Married",
#                 "occupation": "Salaried",
#                 "source_of_wealth": "Business",
#                 "income_range": "1L to 5L",
#                 "cob": "India",
#                 "pob": "Kochi",
#                 "political_exposure": "no_exposure",
#                 "india_tax_residency_status": "resident",
#                 "mode_of_holding": "single",
#                 "ca_line": "hfjfk jifl jffj"
#             }
            
#             res = requests.post(url, json=user_kyc_data)
#             if res.status_code != 200:
#                 return {'success': False, 'error': f'Form submission failed with status {res.status_code}'}
            
#             resp_json = res.json()
#             submission_id = resp_json.get('submission_id')
#             if not submission_id:
#                 return {'success': False, 'error': 'Submission ID missing from form response'}
            
#             # Store submission ID
#             SubmissionID.objects.create(
#                 transaction=obj.transaction,
#                 submission_id=submission_id,
#                 message_id=message_id,
#                 timestamp=timestamp
#             )
            
#             # Continue with the rest of form submission logic...
#             # (Include the full payload construction from your FormSubmisssion view)
            
#             return {'success': True, 'message_id': message_id, 'submission_id': submission_id}
            
#         except Exception as e:
#             return {'success': False, 'error': str(e)}
    
#     def _execute_init(self, transaction_id, bpp_id, bpp_uri, message_id):
#         """Execute init step"""
#         # Implementation similar to your INIT view
#         try:
#             # Your existing INIT logic here
#             return {'success': True, 'message_id': str(uuid.uuid4())}
#         except Exception as e:
#             return {'success': False, 'error': str(e)}
    
#     def _wait_for_on_init(self, transaction_id, timeout=30):
#         """Wait for on_init callback"""
#         start_time = time.time()
#         while time.time() - start_time < timeout:
#             try:
#                 transaction = Transaction.objects.get(transaction_id=transaction_id)
#                 init_entry = OnInitSIP.objects.filter(transaction=transaction).first()
#                 if init_entry:
#                     payload = init_entry.payload
#                     return {
#                         'bpp_id': payload['context']['bpp_id'],
#                         'bpp_uri': payload['context']['bpp_uri'],
#                         'message_id': payload['context']['message_id'],
#                         'payload': payload
#                     }
#             except:
#                 pass
#             time.sleep(2)
#         return None
    
#     def _execute_confirm(self, transaction_id, bpp_id, bpp_uri, message_id):
#         """Execute confirm step"""
#         # Implementation similar to your ConfirmSIP view
#         try:
#             # Your existing ConfirmSIP logic here
#             return {'success': True, 'message_id': str(uuid.uuid4())}
#         except Exception as e:
#             return {'success': False, 'error': str(e)}
    
#     def _wait_for_on_confirm(self, transaction_id, timeout=30):
#         """Wait for on_confirm callback"""
#         start_time = time.time()
#         while time.time() - start_time < timeout:
#             try:
#                 transaction = Transaction.objects.get(transaction_id=transaction_id)
#                 confirm_entry = OnConfirm.objects.filter(transaction=transaction).first()
#                 if confirm_entry:
#                     return {
#                         'order_details': confirm_entry.payload.get('message', {}).get('order', {}),
#                         'payload': confirm_entry.payload
#                     }
#             except:
#                 pass
#             time.sleep(2)
#         return None


# # URL Configuration
# # Add this to your urls.py
# from django.urls import path

# urlpatterns = [
#     # ... your existing URLs
#     path('api/complete-sip-flow/', CompleteSIPFlowView.as_view(), name='complete-sip-flow'),
# ]