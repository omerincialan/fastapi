from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import models, schemas, auth2
from .. database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(auth2.get_current_user),
              Limit:int = 10, skip : int = 0,
              search : Optional[str] = "" ):
    
    #this line allows only the post belonging to logged in user to be retrieved
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    print(Limit, search)

    # here we added limit to see # of posts, skip for pagination
    # and 
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    # here is the SQL for this line of code
    # select posts.*, count(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id = votes.post_id group by posts.id;
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    # this is the SQL command to debug and follow
    print(posts)

    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    return posts



@router.get("/user", response_model=List[schemas.Post])
def get_posts_user(db: Session = Depends(get_db),
              current_user: int = Depends(auth2.get_current_user)):
    
    #this line allows only the post belonging to logged in user to be retrieved
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    #this line allows all posts to be retrieved 
    #posts = db.query(models.Post).all()

    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(auth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s ) RETURNING * """, (post.title, post.content, post.published)) # order matters
    # new_post = cursor.fetchone()  
    # conn.commit() #this is a must to finalize the change
    
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# title: string, content : string, category etc


@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, response:Response, 
             db: Session = Depends(get_db),
             current_user: int = Depends(auth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    #post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #    models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    #).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not auhoized to perform the requested action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), 
                current_user: int = Depends(auth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s RETURNING * """ , (str(id),))
    # deleted_post = cursor.fetchone()
    
    # conn.commit()
    # deleting post
    # find the index
    # than pop that

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not auhoized to perform the requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, updated_post : schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: int = Depends(auth2.get_current_user)):
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    #this is the query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # this is the actual post to update
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform this action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
