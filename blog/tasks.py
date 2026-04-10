from celery import shared_task

@shared_task
def notify_new_post(post_title, owner_username):
    print(f'📧 New post "{post_title}" created by {owner_username}!')
    print(f'Notification sent to all subscribers!')
    return f'Notification sent for post: {post_title}'