from selenium import webdriver
import time

class Oscars:
    
    def __init__(self):
        pass
    
    def scrape(self):
        web = webdriver.Chrome('./chrome/chromedriver.exe')
        web.get('https://awardsdatabase.oscars.org/')

        time.sleep(5)

        category_button = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/button')
        category_button.click()

        direction_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[12]/a/label')
        writing_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[28]/a/label')
        best_picture_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[22]/a/label')
        actor_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[4]/a/label')
        actress_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[6]/a/label')
        s_actor_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[5]/a/label')
        s_actress_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[1]/div[2]/div/span/div/ul/li[7]/a/label')

        direction_checkbox.click()
        writing_checkbox.click()
        best_picture_checkbox.click()
        actor_checkbox.click()
        actress_checkbox.click()
        s_actor_checkbox.click()
        s_actress_checkbox.click()
        
        year_from_button = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[1]/span/div/button')
        year_from_button.click()
        from_year_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[1]/span/div/ul/li[22]/a/label')
        from_year_checkbox.click()

        year_to_button = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[2]/span/div/button')
        year_to_button.click()
        to_year_checkbox = web.find_element_by_xpath('//*[@id="basicsearch"]/div/div[2]/div[2]/div/div[2]/span/div/ul/li[6]/a/label')
        to_year_checkbox.click()

        submit_button = web.find_element_by_xpath('//*[@id="btnbasicsearch"]')
        submit_button.click()

        find_year_results = web.find_elements_by_css_selector('.awards-result-chron')

        oscars_dict = {}
        oscars_dict["oscar_ceremonies"] = [] 

        for year_element in find_year_results:
            award_header_text = year_element.find_element_by_css_selector('a.nominations-link').text
            #print(award_header_text)
            subgroups = year_element.find_elements_by_css_selector('.result-subgroup')
            ceremony_dict = {}
            title_split_arr = award_header_text.split(" ")
            #print(title_split_arr)
            year = title_split_arr[0]
            index = title_split_arr[1]
            ceremony_dict["year"] = year
            ceremony_dict["index"] = index
            oscars_dict["oscar_ceremonies"].append(ceremony_dict)

            directing_dict = {}
            acting_dict = {}
            acting_female_dict = {}
            s_acting_dict = {}
            s_acting_female_dict = {}
            best_picture_dict = {}
            writing_adapted_dict = {}
            writing_original_dict = {}

            ceremony_dict["directing"] = directing_dict
            ceremony_dict["acting"] = acting_dict
            ceremony_dict["acting_female"] = acting_female_dict
            ceremony_dict["support_acting"] = s_acting_dict
            ceremony_dict["support_acting_female"] = s_acting_female_dict
            ceremony_dict["best_picture"] = best_picture_dict
            ceremony_dict["writing_adapted"] = writing_adapted_dict
            ceremony_dict["writing_original"] = writing_original_dict

            directing_dict["nominations"] = []
            directing_dict["winner"] = {}

            acting_dict["nominations"] = []
            acting_dict["winner"] = {}
            
            acting_female_dict["nominations"] = []
            acting_female_dict["winner"] = {}
            
            s_acting_dict["nominations"] = []
            s_acting_dict["winner"] = {}
            
            s_acting_female_dict["nominations"] = []
            s_acting_female_dict["winner"] = {}

            best_picture_dict["nominations"] = []
            best_picture_dict["winner"] = {}

            writing_adapted_dict["nominations"] = []
            writing_adapted_dict["winner"] = {}

            writing_original_dict["nominations"] = []
            writing_original_dict["winner"] = {}

            for subgroup in subgroups:
                subgrp_title = subgroup.find_element_by_css_selector('.result-subgroup-title a.nominations-link').text
#                 print(subgrp_title)
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
                    elif subgrp_title == "ACTOR IN A LEADING ROLE":
                        actor = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        size = len(movie)
                        acting_dict["nominations"].append({"movie" : movie, "actor" : actor})
                        if is_winner:
                            acting_dict["winner"] = {"movie" : movie, "actor" : actor}
                    elif subgrp_title == "ACTRESS IN A LEADING ROLE":
                        actress = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        size = len(movie)
                        acting_female_dict["nominations"].append({"movie" : movie, "actress" : actress})
                        if is_winner:
                            acting_female_dict["winner"] = {"movie" : movie, "actress" : actress}
                    elif subgrp_title == "ACTOR IN A SUPPORTING ROLE":
                        s_actor = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        s_acting_dict["nominations"].append({"movie" : movie, "actor" : s_actor})
                        if is_winner:
                            s_acting_dict["winner"] = {"movie" : movie, "actor" : s_actor}
                    elif subgrp_title == "ACTRESS IN A SUPPORTING ROLE":
                        s_actress = result.find_element_by_css_selector('.awards-result-nomination .awards-result-nominationstatement').text
                        s_acting_female_dict["nominations"].append({"movie" : movie, "actress" : s_actress})
                        if is_winner:
                            s_acting_female_dict["winner"] = {"movie" : movie, "actress" : s_actress}
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

        web.close()
        return oscars_dict