from selenium import webdriver
import time

class Oscars:
    
    def __init__(self):
        pass
    
    def scrape(self):
        web = webdriver.Chrome('C:/Users/palag/Downloads/chromedriver_win32/chromedriver.exe')
        web.get('https://awardsdatabase.oscars.org/')

        time.sleep(5)

        category_button = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/button')
        category_button.click()

        direction_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[12]/a/label')
        writing_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[28]/a/label')
        best_picture_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[22]/a/label')
        music_original_score_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[20]/a/label')

        direction_checkbox.click()
        time.sleep(3)
        writing_checkbox.click()
        time.sleep(3)
        best_picture_checkbox.click()
        time.sleep(3)
        music_original_score_checkbox.click()

        year_from_button = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[1]/span/div/button')
        year_from_button.click()
        time.sleep(3)
        from_year_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[1]/span/div/ul/li[15]/a/label')
        from_year_checkbox.click()
        time.sleep(3)

        year_to_button = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[2]/span/div/button')
        year_to_button.click()
        time.sleep(3)
        to_year_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[2]/span/div/ul/li[6]/a/label')
        to_year_checkbox.click()
        time.sleep(3)

        submit_button = web.find_element_by_xpath('//*[@id="btnbasicsearch"]')
        submit_button.click()

        time.sleep(5)

        find_year_results = web.find_elements_by_css_selector('.awards-result-chron')

        oscars_dict = {}
        oscars_dict["oscar_ceremonies"] = [] 

        for year_element in find_year_results:
            award_header_text = year_element.find_element_by_css_selector('a.nominations-link').text
            print(award_header_text)
            subgroups = year_element.find_elements_by_css_selector('.result-subgroup')
            ceremony_dict = {}
            title_split_arr = award_header_text.split(" ")
            print(title_split_arr)
            year = title_split_arr[0]
            index = title_split_arr[1]
            ceremony_dict["year"] = year
            ceremony_dict["index"] = index
            oscars_dict["oscar_ceremonies"].append(ceremony_dict)

            directing_dict = {}
            muscic_director_dict = {}
            best_picture_dict = {}
            writing_adapted_dict = {}
            writing_original_dict = {}

            ceremony_dict["directing"] = directing_dict
            ceremony_dict["music"] = muscic_director_dict
            ceremony_dict["best_picture"] = best_picture_dict
            ceremony_dict["writing_adapted"] = writing_adapted_dict
            ceremony_dict["writing_original"] = writing_original_dict

            directing_dict["nominations"] = []
            directing_dict["winner"] = {}

            muscic_director_dict["nominations"] = []
            muscic_director_dict["winner"] = {}

            best_picture_dict["nominations"] = []
            best_picture_dict["winner"] = {}

            writing_adapted_dict["nominations"] = []
            writing_adapted_dict["winner"] = {}

            writing_original_dict["nominations"] = []
            writing_original_dict["winner"] = {}

            for subgroup in subgroups:
                subgrp_title = subgroup.find_element_by_css_selector('.result-subgroup-title a.nominations-link').text
                print(subgrp_title)
                award_result_details = subgroup.find_elements_by_css_selector('.awards-result-subgroup-items .result-details')

                for result in award_result_details:
                    movie = result.find_element_by_css_selector('.awards-result-nomination .awards-result-film').text
                    glyphicon = result.find_elements_by_css_selector('span.glyphicon.glyphicon-star')
                    is_winner = False
                    if len(glyphicon) == 1:
                        is_winner = True
                    if subgrp_title == "DIRECTING":
                        director = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        directing_dict["nominations"].append({"movie" : movie, "director" : director})
                        if is_winner:
                            directing_dict["winner"] = {"movie" : movie, "director" : director}
                        #print(movie + "-" + director + "-" + str(is_winner))

                    elif subgrp_title == "MUSIC (Original Score)":
                        music_director = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        size = len(movie)
                        muscic_director_dict["nominations"].append({"movie" : movie[:size-3], "music_director" : music_director})
                        if is_winner:
                            muscic_director_dict["winner"] = {"movie" : movie[:size-3], "music_director" : music_director}
                        #print(movie + "-" + music_director + "-" + str(is_winner))

                    elif subgrp_title == "BEST PICTURE":
                        best_picture_dict["nominations"].append({"movie" : movie})
                        if is_winner:
                            best_picture_dict["winner"] = {"movie" : movie}

                    elif subgrp_title == "WRITING (Adapted Screenplay)":
                        writer_adapted = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        writing_adapted_dict["nominations"].append({"movie" : movie, "writer" : writer_adapted})
                        if is_winner:
                            writing_adapted_dict["winner"] = {"movie" : movie, "writer" : writer_adapted}
                        #print(movie + "-" + writer_adapted + "-" + str(is_winner))

                    elif subgrp_title == "WRITING (Original Screenplay)":
                        writer_original = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        writing_original_dict["nominations"].append({"movie" : movie, "writer" : writer_original})
                        if is_winner:
                            writing_original_dict["winner"] = {"movie" : movie, "writer" : writer_original}
                        #print(movie + "-" + writer_original + "-" + str(is_winner))

        print(oscars_dict)
        web.close()