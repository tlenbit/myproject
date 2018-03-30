import React from 'react';
import ReactDOM from 'react-dom';


    export default class BaseRoom extends React.Component {
        constructor(props) {
	    super(props);
	    this.state = {
		playingEntry: {title: '', id: -1},
	        playlistEntries: [],
		usersList: [],
		artistSearchSuggestions: [],
		trackSearchSuggestions: []
	    };
	    this.setNextPlayingEntry = this.setNextPlayingEntry.bind(this);
	    this.addPlaylistEntry = this.addPlaylistEntry.bind(this);
	    this.getArtistSuggestions = this.getArtistSuggestions.bind(this);
            this.getTrackSuggestions = this.getTrackSuggestions.bind(this);
	}
	componentDidMount() {
	    this.socket = new WebSocket("ws://" + window.location.host + '/ws' + window.location.pathname);
	    this.socket.onmessage = e => {
	        // info on new users and tracks votes comes through ws messages
	        let parsedData = JSON.parse(e.data)
	        if ('playlist' in parsedData) {
	            this.setState({
			    playlistEntries: parsedData['playlist']['entries']
                                .sort((a, b) => {
                                    var x = a.rating; var y = b.rating;
                                    return ((x < y) ? 1 : ((x > y) ? -1 : 0));
                                })
		    });
		    this.setState({playingEntry: parsedData['playlist']['playing_entry']});
                }
	        if ('users' in parsedData) {
	            this.setState({usersList: parsedData['users']});
	        }
	        if ('chat' in parsedData) {
	            //this.setState({incomeChatMessage: parsedData['chat_message']});
	        }
	        if ('search' in parsedData) {
		    if ('artist_suggestions' in parsedData['search']) {
	                this.setState({
				artistSearchSuggestions: parsedData['search']['artist_suggestions']
			});
		     }
                     if ('track_suggestions' in parsedData['search']) {
	                this.setState({
				trackSearchSuggestions: parsedData['search']['track_suggestions']
			});

		    }
		    //if (this.state.playingEntry.id == -1) {
		        //this.setNextPlayingEntry();
		    //}
                }
	    }
	}
	componentWillUnmount() {
	    console.log('UNMOUNTING ROOT');
	    this.ws.close();
	}
	setNextPlayingEntry() {
            if (this.state.playingEntry.id != -1) {
	        let info = {};
	        info['playlist'] = {};
		info['playlist']['set_next_playing_entry'] = true;
	        this.socket.send(JSON.stringify(info));
            }
	}
	addPlaylistEntry(artistId, trackId) {
	    let info = {};
	    info['playlist'] = {};
	    info['playlist']['add_entry'] = {};
	    info['playlist']['add_entry']['track_id'] = trackId;
	    info['playlist']['add_entry']['artist_id'] = artistId;
	    this.socket.send(JSON.stringify(info));
	}
	getArtistSuggestions(partialArtistName, trackChoice) {
	    //console.log(this.state.artistSearchSuggestions);
	    let info = {}
	    //info['search']['partial_track_title'] = partialTrackTitle;
	    info['search'] = {};
	    info['search']['get_artist_suggestions'] = {}
	    info['search']['get_artist_suggestions']['partial_artist_name'] = partialArtistName;
	    info['search']['get_artist_suggestions']['track_choice_title'] = trackChoice;
	    this.socket.send(JSON.stringify(info));
	}
        getTrackSuggestions(partialTrackTitle, artistChoice) {
	    //console.log(this.state.artistSearchSuggestions);
	    let info = {}
	    //info['search']['partial_track_title'] = partialTrackTitle;
	    info['search'] = {};
	    info['search']['get_track_suggestions'] = {}
	    info['search']['get_track_suggestions']['partial_track_title'] = partialTrackTitle;
	    info['search']['get_track_suggestions']['artist_choice_name'] = artistChoice;
	    this.socket.send(JSON.stringify(info));
	}
    }
