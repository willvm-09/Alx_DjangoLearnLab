retrieved_book = Book.objects.get(id=new_book.id)
print(retrieved_book)
#1984 by George Orwell published 1949

# Get all attributes as a dictionary
attributes = Book.__dict__

# Display all attributes
for field, value in attributes.items():
    print(f"{field}: {value}")
