from app.db.session import SessionLocal
from app.models import Tag

def create_tags():
    db = SessionLocal()
    
    tags = ['UI', 'Backend', 'Performance']
    created_tags = []
    
    try:
        for tag_name in tags:
            existing_tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not existing_tag:
                new_tag = Tag(name=tag_name)
                db.add(new_tag)
                created_tags.append(tag_name)
        
        db.commit()
        if created_tags:
            print(f"Tags created successfully: {', '.join(created_tags)}")
        else:
            print("All tags already exist. No new tags created.")
    except Exception as e:
        print(f"Error occurred while creating tags: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tags()