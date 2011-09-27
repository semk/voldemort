## Voldemort

Voldemort is a simple static site generator using Jinja2 and markdown templates.

## Installation

    sudo python setup.py install

## Usage Options

    Usage: voldemort [options]
    
    Options:
      -h, --help            show this help message and exit
      -w WORK_DIR, --work_dir=WORK_DIR
                            Working Directory
      -s, --serve           Start the HTTP Server
      -p PORT, --port=PORT  Port inwhich the HTTPServer should run
      -d, --deploy          Deploy this website
      -a AT, --at=AT        Server address to deploy the site
      -t TO, --to=TO        Deployment directory

## Usage Example

Go to the example directory
	cd example

and run
	voldemort

start the HTTPServer
	voldemort --serve --port 8080

Open your browser and see the website in action.

## Writing posts

Posts mainly contain 2 sections. Config section and the Template section. All data inside two `---` contributes the config area and are validated as YAML data. You can set your post related attributes here. In template section you can use Jinja2 templates or Markdown in `{% markdown %} {% endmarkdown %}` blocks.

## Global variables

	posts:		A list of all your posts. All attributes in the YAML section 
				can be accessed either using . or []. 
				eg. post['date'], `post.date
	paginator:	You can paginate your posts using this object.
				eg: {% for post in paginator.posts %}
	post:		Info about the post. Only accessible in post templates.
	page:		Info about a page. Only available in pages other than posts.

## Developer

Sreejith K <sreejithemk@gmail.com>

http://foobarnbaz.com
