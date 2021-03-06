/*********************************************************** 
    On homepage, show episodes which were released today
    and will be released tomorrow

    __version__ = 'v0.1.6'

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
function episodesReleasedToday(day, month, today) {

    current_date = day + '.' + month + '. '
    console.log("Current date: " + current_date)

    const td_elements = document.getElementsByTagName("td")
    const td_array = [].slice.call(td_elements)

    // Date format: 5.10., 10.10., 21.10. etc.
    const date_regex = /(\d){0,2}\.(\d){0,2}\./g;
    const date_regex2 = /(\d{1,2}\.\d{1,2}\.) /g;

    // Go through all of the "td" elements in html code (array)
    td_array.forEach(function(td_array_item) {
        let td_element_html = td_array_item.innerHTML

        //console.log(td_element_html)
        
        var i = 0;
        let td_date_match;

        var td_date_statement = false;

        // Search through all matches and break from loop
        // if match is equal to current day
        // TODO: what happens if tv shows released more epidoes per day? FIX IT!!
        while ( td_date_match = date_regex2.exec(td_element_html)) {

            if (td_date_match != null && td_date_match[i] == current_date) {
                td_date_statement = true;
                break;
            }

            i += 1
        }

        if ( td_date_statement ) {

            // Find the date when episode was released
            let episode_date = td_date_match[0]

            // Find class name of each TV show (and its episodes)
            let div_episodes_class = nthParent(td_array_item, 4).className //item.parentNode.parentNode.parentNode.parentNode.className

            // Episode must be released today 
            // and have class "episodes-bg active" to be shown on homepage
            if ( div_episodes_class.includes('active')) {

                todays_episode_element = td_array_item.parentNode.innerHTML
                todays_episode_node = td_array_item.parentNode
                console.log("todays_episode_node: ", todays_episode_node);

                let tvshow_name = todays_episode_node.getElementsByTagName('a')[0].getAttribute('title')
                console.log('tvshow_name: ', tvshow_name)

                // Hotfix for duplicate elemenets to be skipped. 
                // kinda hacky way, but hey.. it works :-)
                //let td_id = 'snippet--episodes {0}'.format(tvshow_name)

                // If episode is already on homepage, continue with forEach loop
                //console.log('td_id: ', td_id)
                //console.log('todays_episode_node.parentNode.id: ', todays_episode_node.parentNode.getAttribute('id'))
                // if (todays_episode_node.parentNode.id == td_id) {
                //     return;
                // }

                // Get name of the TV Show
                let title = nthParent(todays_episode_node, 3).children[0].textContent
                console.log(title)

                var tvshows_div_name = ''
                var margin = ''

                if (today == true) {
                    tvshows_div_name = 'tvshows_today'
                    margin = '0'

                } else {
                    tvshows_div_name = 'tvshows_tomorrow'
                    margin = '15%'
                }

                // Create html elements for TV shows' episode
                let h2_element = document.createElement('h2')
                let h2_title_node = document.createTextNode(title)
                h2_element.appendChild(h2_title_node)
                let div_tvshows_today = document.getElementById(tvshows_div_name)
                div_tvshows_today.appendChild(h2_element)
                div_tvshows_today.style.marginBottom = margin

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

var today = new Date()
var current_date = today.getDate()
var current_month = today.getMonth()+1

today.setDate(today.getDate() + 1)
var tomorrow_date = today.getDate()
var tomorrow_month = today.getMonth()+1

var today = true

episodesReleasedToday(current_date, current_month, today)
episodesReleasedToday(tomorrow_date, tomorrow_month, today = false)







