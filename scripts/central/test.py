""" import mariadb

# Create a connection to the remote MariaDB database
conn = mariadb.connect(host='10.10.2.3', port=3306, user='py_interface', password='sshDB#532', database='')

# Create a cursor object
cur = conn.cursor()

print("Writing query")

# Write the query
query = "INSERT INTO emails (email, password) VALUES (danATsampletext.com, passwd)"

# Execute the query
cur.execute(query)

print("Query Executed on remote")

# Close the cursor and connection
cur.close()
conn.close() """

from db_nas_connection import DbNasConnection

# constants
# platforms:
TIKTOK = "tiktok"
YOUTUBE_SHORT = "yt_shorts"
YOUTUBE_VIDEO = "yt_videos"
REELS = "instagram_reels"
    
# media types:
VIDEO = "video"
AUDIO = "audio"
TEXT = "text"
IMAGE = "image"


def main():
    dbObj = DbConnection()
    print(dbObj.credentials)
    dbObj.write_account('danny@thing.com', YOUTUBE_SHORT, 'jonnyTalks', 'ISHIT')
    

main()