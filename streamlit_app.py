import os
import streamlit as st
import markdown # type: ignore
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="My Blog",
    page_icon="📝",
    layout="centered"
)

# Add custom CSS
st.markdown("""
<style>
.blog-post img {
    max-width: 100%;
    height: auto;
    margin: 1rem 0;
}
.blog-post blockquote {
    border-left: 3px solid #ccc;
    margin: 1rem 0;
    padding-left: 1rem;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

def get_posts():
    """Get all markdown posts with metadata"""
    posts = []
    for filename in os.listdir('posts'):
        if filename.endswith('.md'):
            with open(os.path.join('posts', filename), 'r') as file:
                content = file.read()
                md = markdown.Markdown(extensions=['meta'])
                html = md.convert(content)

                # Extract metadata or use defaults
                title = md.Meta.get('title', [filename[:-3]])[0]
                date_str = md.Meta.get('date', [datetime.now().strftime('%Y-%m-%d')])[0]
                description = md.Meta.get('description', [''])[0]

                posts.append({
                    'slug': filename[:-3],
                    'title': title,
                    'date': datetime.strptime(date_str, '%Y-%m-%d'),
                    'description': description,
                    'content': html
                })

    return sorted(posts, key=lambda x: x['date'], reverse=True)

def main():
    st.title("My Blog")
    
    # Add search box in the sidebar
    search_query = st.sidebar.text_input("Search posts...", "")
    
    posts = get_posts()
    
    # Filter posts if search query exists
    if search_query:
        search_query = search_query.lower()
        posts = [
            post for post in posts
            if search_query in post['title'].lower() or 
               search_query in post['description'].lower() or 
               search_query in post['content'].lower()
        ]
        st.sidebar.write(f"Found {len(posts)} results")
    
    # Create tabs for Home and individual posts
    tabs = ["Home"] + [post['title'] for post in posts if 'slug' in st.experimental_get_query_params()]
    current_tab = st.tabs(tabs)[0]
    
    # Check if a specific post is requested via query parameters
    query_params = st.experimental_get_query_params()
    selected_slug = query_params.get('slug', [None])[0]
    
    if selected_slug:
        # Display specific post
        for post in posts:
            if post['slug'] == selected_slug:
                st.title(post['title'])
                st.write(f"Published on {post['date'].strftime('%B %d, %Y')}")
                st.markdown(post['content'], unsafe_allow_html=True)
                if st.button("← Back to Posts"):
                    st.experimental_set_query_params()
                    st.rerun()
                break
    else:
        # Display post list
        for post in posts:
            st.markdown("---")
            st.subheader(post['title'])
            st.write(f"Published on {post['date'].strftime('%B %d, %Y')}")
            if post['description']:
                st.write(post['description'])
            if st.button("Read More", key=post['slug']):
                st.experimental_set_query_params(slug=post['slug'])
                st.rerun()

if __name__ == "__main__":
    main()
