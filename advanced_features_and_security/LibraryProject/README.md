This is the first Django Project. 

In this project, I started by creating permissions such as can_view, can_create, can_edit, and can_delete within the Author Model.
I then created three groups in my models.py file - admins_groups, editors_groups, and viewers_groups. 
After that, I fetched the content type, which is the Author Model in my models.py file. 
I then assigned permissions to my groups. The admins_group got the permissions "can_view, can_create, can_edit, and can_delete"
The editors_group got the permissions "can_create, can_edit"
While the viewers_group got the "can_view" permission only. 
I then saved the groups.

In my views.py file, I created my views to check for these permissions before allowing users to perform certain actions. 
I ensured that views that create, edit, or delete model instances check for the correct permissions.
