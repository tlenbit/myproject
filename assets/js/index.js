import React from 'react';
import ReactDOM from 'react-dom';
import ReactPlayer from 'react-player';


    class UsersList extends React.Component {
        render() {
	    const rows = this.props.usersList.map((user) =>
	        <p key={user.name}>
		    {user.name}
		</p>
            );
	    return (
		<div id="users" className="users">
		Users in da room:
		    {rows}
		</div>
	    );
	}
    }
    
    class VoteButton extends React.Component {
        constructor(props) {
            super(props);
            this.voteForTrack = this.voteForTrack.bind(this);
	    this.UP_or_DOWN = this.props.U_or_D == "U" ? "UP" : "DOWN";
        }
        voteForTrack() {
            var info = {};
	    info["playlist"] = {}
            info["playlist"]["vote"] = {};
	    info["playlist"]["vote"]["entry_id"] = this.props.entry_id;
            info["playlist"]["vote"]["U_or_D"] = this.props.U_or_D;
	    this.props.socket.send(JSON.stringify(info));
        }
        render() {
	    return (
		<input type="button" value={this.UP_or_DOWN} onClick={this.voteForTrack} />
	    );
	}
    }

    class Playlist extends React.Component {
	render() {
	    const rows = this.props.playlistEntries
	        	        .map((entry) => 
		        <p key={entry.id}>
		            <VoteButton entry_id={entry.id} U_or_D="U" socket={this.props.socket}/>
		            <VoteButton entry_id={entry.id} U_or_D="D" socket={this.props.socket}/>
                            {entry.rating} - {entry.title} by <span className="artist_name">{entry.artist}</span>
		        </p>
	                        );
	    return (
	        <div id="playlist" className="playlist">
		    {rows}
	        </div>
	    );
	}
    }
/*
    class Player extends React.Component {
        contructor(props) {
	    super(props)
	    this.state = {

	    }
	    this.onTrackEnd = this.onTrackEnd.bind(this);
	}
	onTrackEnd() {
	    	}
	render() {
	    return (
		<div className="player">
		    <ReactPlayer onEnded={this.} url="https://www.youtube.com/watch?v=AQBh9soLSkI" playing />
		</div>
	}
    }
*/
    class Room extends React.Component {
        constructor(props) {
	    super(props);
	    this.state = {
		playingEntry: {title: '', id: -1},
	        playlistEntries: [],
		usersList: []
	    }
	    this.setNextPlayingEntry = this.setNextPlayingEntry.bind(this)
	}
	componentDidMount() {
	    this.socket = new WebSocket("ws://" + window.location.host + window.location.pathname);
	    this.socket.onmessage = e => {
	        // info on new users and tracks votes comes through ws messages
	        let parsedData = JSON.parse(e.data);
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
	        if ('chat_message' in parsedData) {
	            //this.setState({incomeChatMessage: parsedData['chat_message']});
	        }
		if (this.state.playingEntry.id == -1) {
		    //this.setNextPlayingEntry();
		}
            }
	}
	componentWillUnmount() {
	    this.ws.close();
	}
	setNextPlayingEntry() {
	    // ask server to delete entry from playlist because it will be played now
            if (this.state.playingEntry.id != -1) {
	        var info = {};
	        info['playlist'] = {};
		info['playlist']['set_next_playing_entry'] = true;
	        this.socket.send(JSON.stringify(info));
            }
	    //var array = this.state.playlistEntries;
	    //var element = this.state.playlistEntries[0];
	    // move top entry to 'playingEntry'
            //array.splice(1, 1);
            //this.setState({playlistEntries: array});
	    //this.setState({playingEntry: element});
	}
        render() {
	    return (
	        <div className="root">
		    Playing: {this.state.playingEntry.title} by {this.state.playingEntry.artist}
		    <input type="button" value="switch_playing_entry" onClick={this.setNextPlayingEntry}/>
	            <Playlist playlistEntries={this.state.playlistEntries} socket={this.socket} />
		    <UsersList usersList={this.state.usersList} />
		</div>
	    );
	}
    }

    ReactDOM.render(
        <Room />,
        document.getElementById('root')
    );
