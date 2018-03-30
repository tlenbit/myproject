import React from 'react';
import ReactDOM from 'react-dom';
import ReactPlayer from 'react-player';
import Select from 'react-select';

import BaseRoom from './BaseRoom';
import {
    Playlist, 
    NewPlaylistEntry, 
    UsersList
} from './CommonRoomComponents';

    class AdminRoom extends BaseRoom {
        render() {
	    return (
	        <div className="root">
		    Playing: 
		        {this.state.playingEntry.title} 
		    by 
		        {this.state.playingEntry.artist}
		    <NewPlaylistEntry 
		        artistSuggestions={this.state.artistSearchSuggestions}
		        trackSuggestions={this.state.trackSearchSuggestions}
		        getArtistSuggestions={this.getArtistSuggestions}
		        getTrackSuggestions={this.getTrackSuggestions}
		        addPlaylistEntry={this.addPlaylistEntry}
		    />
		    <input 
		        type="button" 
		        value="switch_playing_entry" 
		        onClick={this.setNextPlayingEntry}
		    />
	            <Playlist 
		        playlistEntries={this.state.playlistEntries} 
		        socket={this.socket} 
		    />
		    <UsersList 
		        usersList={this.state.usersList} 
		    />
		</div>
	    );
	}
    }

    ReactDOM.render(
        <AdminRoom />,
        document.getElementById('root')
    );
