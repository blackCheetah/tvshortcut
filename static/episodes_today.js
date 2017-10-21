/*********************************************************** 
    On homepage, show episodes which were released today

************************************************************/

// Extending string fucntion
// E.g. '{}'.format(string)
// source code: https://stackoverflow.com/a/25227174
String.prototype.format = function () {
    var args = [].slice.call(arguments);
    return this.replace(/(\{\d+\})/g, function (a){
        return args[+(a.substr(1,a.length-2))||0];
    });
};

// source code: https://stackoverflow.com/a/35130223
function nthParent(element, n) {
    while(n-- && element)  
        element = element.parentNode;
    return element;
}

// Check which episodes were released today and create html elements
// to show them on homepage
function episodesReleasedToday() {

    const today = new Date()
    const dd = today.getDate()
    const mm = today.getMonth()+1

    current_date = dd + '.' + mm + '.'
    console.log("Current date: " + current_date)

    const td_elements = document.getElementsByTagName("td")
    const td_array = [].slice.call(td_elements)

    // Date format: 5.10., 10.10., 21.10. etc.
    const date_regex = /(\d){0,2}\.(\d){0,2}\./g;
    
    // arr.forEach(function(element){
    //     elementHtml = element.innerHTML
    //     console.log(elementHtml)
    // });

    // Go through all of the "td" elements in html code (array)
    td_array.forEach(function(td_array_item) {
        let td_element_html = td_array_item.innerHTML
        let td_date_match = date_regex.exec(td_element_html)

        if (td_date_match != null ) {

            // Find the date when episode was released
            let episode_date = td_date_match[0]

            // Find class name of each TV show (and its episodes)
            let div_episodes_class = nthParent(td_array_item, 4).className //item.parentNode.parentNode.parentNode.parentNode.className

            // Episode must be released today 
            // and have class "episodes-bg margin-extra active" to be shown on homepage
            if (episode_date == current_date && div_episodes_class == 'episodes-bg margin-extra active') {

                todays_episode_element = td_array_item.parentNode.innerHTML
                todays_episode_node = td_array_item.parentNode

                let tvshow_name = todays_episode_node.getElementsByTagName('a').title

                // Hotfix for duplicate elemenets to be skipped. 
                // kinda hacky way, but hey.. it works :-)
                let td_id = 'snippet--episodes {0}'.format(tvshow_name)

                // If episode is already on homepage, continue with forEach loop
                if (todays_episode_node.parentNode.id == td_id) {
                    return;
                }

                // Get name of the TV Show
                let title = nthParent(todays_episode_node, 3).getElementsByTagName('h2')[0].textContent

                // Create html elements for TV shows' episode
                let h2_element = document.createElement('h2')
                let h2_title_node = document.createTextNode(title)
                h2_element.appendChild(h2_title_node)
                let div_tvshows_today = document.getElementById('tvshows_today')
                div_tvshows_today.appendChild(h2_element)
                div_tvshows_today.style.marginBottom = '15%'

                let table_element = document.createElement('table')
                table_element.className = 'episodes'
                let tbody_element = table_element.createTBody()
                tbody_element.id = 'snippet--episodes {0}'.format(tvshow_name) // should contain name of the episode as ID

                tbody_element.insertAdjacentHTML('afterbegin', todays_episode_element)
                div_tvshows_today.appendChild(table_element)
            }
        }
    });

}

episodesReleasedToday()







