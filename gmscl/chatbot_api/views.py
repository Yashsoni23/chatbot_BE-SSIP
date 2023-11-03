from django.http import JsonResponse
from chatbot import answer_question  # Import the chatbot function
from pymongo import MongoClient
from django.core.mail import send_mail
from bson import ObjectId
import json  # Import the json module


# -----------------------------------------------------------------------------------------------


connection_string = "mongodb+srv://yashsoni48678:yashsoni48678@cluster0.9ugqo1y.mongodb.net/gmscl"
client = MongoClient(connection_string)

db = client.get_database()

chat_history_collection = client.get_database().get_collection("chat_history")
appointments_collection = client.get_database().get_collection("appointments")
queries_collection = client.get_database().get_collection("queries")

# -----------------------------------------------------------------------------------------------


def chatbot_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        if user_input:
            response = answer_question(user_input)

            chat_entry = {
                'user_question': user_input,
                'chatbot_response': response,
            }
            chat_history_collection.insert_one(chat_entry)

            return JsonResponse({'response': response})
        else:
            return JsonResponse({'error': 'User input is missing.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def get_chat_history(request):
    if request.method == 'GET':
        # Retrieve the chat history from the MongoDB collection
        chat_history = list(chat_history_collection.find({}))
        chat_history = [
            {**doc, '_id': str(doc['_id'])} for doc in chat_history
        ]
        total_questions = len(chat_history)
        return JsonResponse({'chat_history': chat_history, 'total_questions': total_questions})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


# -----------------------------------------------------------------------------------------------


def make_query(request):
    if request.method == 'POST':
        query_details = json.loads(request.body)
        if request.body is not None:
            queries_collection.insert_one(query_details)
            return JsonResponse({'success': 'query created successfully.'})
        else:
            return JsonResponse({'error': 'Form data is invalid.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def get_all_queries(request):
    if request.method == 'GET':
        # Retrieve the chat history from the MongoDB collection
        query_collection = list(queries_collection.find({}))
        # Convert ObjectId instances to strings
        query_collection = [
            {**doc, '_id': str(doc['_id'])} for doc in query_collection
        ]
        total_queries = len(query_collection)

        return JsonResponse({'queries': query_collection, 'total_queries': total_queries})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def get_unresolved_queries(request):
    if request.method == 'GET':
        # Retrieve unresolved queries from the MongoDB collection
        unresolved_query_collection = list(
            queries_collection.find({'is_resolved': False}))
        # Convert ObjectId instances to strings
        unresolved_query_collection = [
            {**doc, '_id': str(doc['_id'])} for doc in unresolved_query_collection
        ]
        total_unresolved_queries = len(unresolved_query_collection)

        return JsonResponse({'unresolved_queries': unresolved_query_collection, 'total_unresolved_queries': total_unresolved_queries})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def update_query(request, query_id):
    if request.method == 'PUT':
        try:
            query = queries_collection.find_one({'_id': ObjectId(query_id)})

            if query:
                email = query['email']
                phone_number = query['phone_number']
                query_text = query['query']
                is_resolved = query.get('is_resolved', False)

                data = json.loads(request.body.decode('utf-8'))
                new_answer = data.get('answer', '')
                is_resolved = True

                queries_collection.update_one(
                    {'_id': ObjectId(query_id)},
                    {
                        '$set': {
                            'email': email,
                            'phone_number': phone_number,
                            'query': query_text,
                            'is_resolved': is_resolved,
                            'answer': new_answer,
                        }
                    }
                )

                # Send an email response
                send_email_response(email, query_text, new_answer)

                return JsonResponse({'success': 'Query updated and marked as resolved.'})
            else:
                return JsonResponse({'error': 'Query not found.'})
        except Exception as e:
            return JsonResponse({'error': f'Error while updating the query: {str(e)}'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def send_email_response(receiver_email, subject, answer):
    subject = subject
    message = answer
    from_email = 'yashsoni48678@gmail.com'
    recipient_list = [receiver_email]

    send_mail(subject, message, from_email, recipient_list)
    return JsonResponse({'success': 'Response sent via email.'})


def delete_query(request, query_id):
    if request.method == 'DELETE':
        result = queries_collection.delete_one(
            {'_id': ObjectId(query_id)})

        if result.deleted_count == 1:
            return JsonResponse({'success': 'query deleted successfully.'})
        else:
            return JsonResponse({'error': 'query not found or not deleted.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def delete_all_queries(request):
    if request.method == 'DELETE':
        try:
            db.drop_collection("queries")
            return JsonResponse({'success': 'All querys deleted successfully.'})
        except Exception as e:
            return JsonResponse({'error': f'Error while dropping the collection: {str(e)}'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


# -----------------------------------------------------------------------------------------------


def make_appointment(request):
    if request.method == 'POST':
        appointment_details = json.loads(request.body)
        if request.body is not None:
            appointments_collection.insert_one(appointment_details)
            return JsonResponse({'success': 'Appointment created successfully.'})
        else:
            return JsonResponse({'error': 'Form data is invalid.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def get_all_appointments(request):
    if request.method == 'GET':
        # Retrieve the chat history from the MongoDB collection
        appointment_collection = list(appointments_collection.find({}))
        # Convert ObjectId instances to strings
        appointment_collection = [
            {**doc, '_id': str(doc['_id'])} for doc in appointment_collection
        ]
        total_appointment = len(appointment_collection)

        return JsonResponse({'appointments': appointment_collection, 'total_appointments': total_appointment})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def delete_appointment(request, appointment_id):
    if request.method == 'DELETE':
        result = appointments_collection.delete_one(
            {'_id': ObjectId(appointment_id)})

        if result.deleted_count == 1:
            return JsonResponse({'success': 'Appointment deleted successfully.'})
        else:
            return JsonResponse({'error': 'Appointment not found or not deleted.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def delete_all_appointments(request):
    if request.method == 'DELETE':
        try:
            # Drop the "appointments" collection
            db.drop_collection("appointments")
            return JsonResponse({'success': 'All appointments deleted successfully.'})
        except Exception as e:
            return JsonResponse({'error': f'Error while dropping the collection: {str(e)}'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


# -----------------------------------------------------------------------------------------------
