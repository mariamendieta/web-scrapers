from general_utilities import get_html, select_soup, \
                output_data_to_mongo, grab_contents_key

def process_album_title_hrefs(album_title_hrefs, album_titles): 
    '''
    Input: List
    Output: Dictionary

    For each of the inputted hrefs, go to the href and grab the overall 
    critic and user scores. 
    '''
    base_url = 'http://www.albumoftheyear.org'
    final_json_lst = []
    for idx, href in enumerate(album_title_hrefs.values()[0]):
        soup = get_html(base_url + href)
        center_content = select_soup(soup, '#centerContent').values()[0][0]
        user_score = find_user_score(center_content)
        critic_score = find_critic_score(center_content)
        json_dct = {'Album Title': album_titles[idx], "User Score": user_score, 
                    "Critic Score": critic_score}

        final_json_lst.append(json_dct)

    return final_json_lst

def find_user_score(center_content): 
    '''
    Input: bs4.element.Tag
    Output: Integer

    Parse the elements in the inputted bs4.element.Tag to grab the 
    average user score for the inputted album. 
    '''

    center_content_txt = center_content.text
    user_score_idx = center_content_txt.find('USER SCORE') 
    beg_idx, end_idx = user_score_idx + 10, user_score_idx + 12
    user_score = int(center_content_txt[beg_idx:end_idx])

    return user_score

def find_critic_score(center_content): 
    '''
    Input: bs4.element.Tag
    Output: Integer

    Parse the elements in the inputted bs4.element.Tag to grab the 
    average critic score for the inputted album. 
    '''
    center_content_txt = center_content.text
    critic_score_idx = center_content_txt.find('CRITIC SCORE') 
    beg_idx, end_idx = critic_score_idx + 12, critic_score_idx + 14
    critic_score = center_content_txt[beg_idx:end_idx]

    return critic_score

if __name__ == '__main__': 
    URL = 'http://www.albumoftheyear.org/list/summary/2015/'
    soup = get_html(URL) 

    css_selectors = ['.albumTitle']
    album_titles_contents = select_soup(soup, css_selectors)
    album_titles = grab_contents_key(album_titles_contents, 'text').values()[0]
    album_title_links = grab_contents_key(album_titles_contents, 'a')
    album_title_hrefs = grab_contents_key(album_title_links, 'href')

    final_json_lst = process_album_title_hrefs(album_title_hrefs, album_titles)
    output_data_to_mongo(final_json_lst, 'music', 'music_lists', 
            keys=["Album Title"])



