import pytumblr
import json
import time
from tqdm import tqdm


class GetTumblrImagesURLs:

    __images = []
    __images_to_skip = []
    ___config = None

    def __init__(self, blog_name, limit, skip_downloaded_images=True):
        with open('../config_auth.json') as f:
            self.__config = json.load(f)
        self.__images_to_skip = self.__load_image_list('../downloaded_images.json')
        self.__images = self.__get_urls_to_images(blog_name, limit, skip_images=skip_downloaded_images)
        self.__save_image_list('../downloaded_images.json')

    def __getitem__(self, index):
        return self.__images[index]

    def __len__(self):
        return len(self.__images)

    def __get_urls_to_images(self, blog_name, limit=0, skip_images=True):
        __client = self.__initialize_tumblr_client()

        downloaded_posts = 0
        result = []

        posts = __client.posts(blog_name, type='photo', limit=1, offset=0)

        if limit == 0:
            total_posts = posts['total_posts']
        else:
            total_posts = limit

        offset = 0

        while offset < total_posts:
            posts = __client.posts(blog_name, type='photo', limit=20, offset=offset)
            for key in posts:
                if key == "posts":
                    for post in posts[key]:
                        for item in [item for item in post.keys() if item == 'photos']:
                            for item2 in post[item]:
                                if skip_images:
                                    if item2['original_size']['url'] not in self.__images_to_skip:
                                        result.append(item2['original_size']['url'])
                                else:
                                    result.append(item2['original_size']['url'])
            offset += 20
        return result

    def __initialize_tumblr_client(self):
        __client = pytumblr.TumblrRestClient(
            self.__config['Tumblr']['REST_SECRET_1'],
            self.__config['Tumblr']['REST_SECRET_2'],
            self.__config['Tumblr']['REST_SECRET_3'],
            self.__config['Tumblr']['REST_SECRET_4'])
        return __client

    def __save_image_list(self, outputfilename):
        with open(outputfilename, 'w') as outfile:
            outfile.write(json.dumps(self.__images))

    def __load_image_list(self, inputfile):
        with open(inputfile, 'r') as infile:
            return json.load(infile)

    def __check_if_images_from_list_exists_in_folder(self):
        raise NotImplementedError

    def getfollowedblogs(self, limit=0):
        __client = self.__initialize_tumblr_client()
        result = []

        offset = 0
        i = 0
        if limit == 0:
            total_blogs = __client.following()['total_blogs']
        else:
            total_blogs = limit

        pbar = tqdm(total=total_blogs)

        while i < total_blogs:
            response = __client.following(**{'limit': 20, 'offset': offset})

            if 'meta' in response.keys():
                attempt = 1
                while response['meta']['status'] == 429:
                    print ('Conn problem, retrying...')
                    response = __client.following(**{'limit': 20, 'offset': offset})
                    attempt += 1
                    if attempt >= 10:
                        raise ConnectionRefusedError(response['meta']['status'] + ": " + response['meta']['msg'])
                    time.sleep(attempt*2)
            blogs = response['blogs']
            for blog in blogs:
                result.append(blog['url'])
                i += 1
                pbar.update(1)

            offset += 20


        return result
