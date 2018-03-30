import React from 'react';
import ReactDOM from 'react-dom';
import Select from 'react-select';

import './react-select/select.scss';
import './react-select/default.scss';
//import './react-select/components.scss';
//import './react-select/control.scss';
//import './react-select/menu.scss';
import './react-select/mixins.scss';
//import './react-select/multi.scss';
import './react-select/spinner.scss';

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
    //TODO: move voteForTrack to upper component
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
   class NewPlaylistEntry extends React.Component {
        constructor(props) {
	    super(props);
	    this.state = {
		artistChoice: {value: '', label: ''},
		trackChoice: {value: '', label: ''}
	    }
	}
        render() {
	    return (
		<div className='search'>
		    <Select
		        name='artistSearch'
		        value={this.state.artistChoice}
		        searchable={true}
		        resetValue={{value: '', label: ''}}
		        options={this.props.artistSuggestions}
		        onFocus={
			    () => {
			        //if (this.state.trackChoice.value) {
				    console.log('artist search focused');
				    //console.log('');
			            this.props.getArtistSuggestions('', this.state.trackChoice.label);
				//}
			    } 
			}
		        onInputChange={
			    (input) => {
				console.log('onInputChange', input, this.state.trackChoice.label);
				// searching for artists only by 1 letter is pointless (yet)
				if (this.state.trackChoice.label != '' || input.length>1) {
			            this.props.getArtistSuggestions(input, this.state.trackChoice.label);
				}
			    } 
			}
		        onChange={ 
			    (input) => {
				if (input != null) {
                                    console.log('onChange');
		                    this.setState({artistChoice: input}) 
                                    this.props.getTrackSuggestions('', input.label);
				}
			    }
		        }
		    />
		    <Select 
		        name='trackSearch'
		        value={this.state.trackChoice}
		        searchable={true}
		        resetValue={{value: '', label: ''}}
		        options={this.props.trackSuggestions}
		        onFocus={
			    () => {
			        //if (this.state.artistChoice.value) {
				    console.log('track search focused');
			            this.props.getTrackSuggestions('', this.state.artistChoice.label);
				//}
			    } 
			}
		        onInputChange={
			    (input) => {
				//console.log(this.state.artistChoice, input);
				if (this.state.artistChoice.label != '' || input.length>1) {
			            this.props.getTrackSuggestions(input, this.state.artistChoice.label)
				}
			    } 
			}
		        onChange={ 
			    (input) => {
				if (input != null) {
		                    this.setState({trackChoice: input});
                                    this.props.getArtistSuggestions('', input.label);
				}
			    }
		        }
		    />
		    <input
		        type='button'
		        value='add'
		        disabled={(this.state.artistChoice.value & this.state.trackChoice.value)? false: true}
		        className="btn btn-primary"
		        onClick={ 
		            () => {
                                  //console.log(this.artistChoice.label+this.artistChoice.value);
				  //console.log(this.trackChoice.label+this.trackChoice.value);
	                          this.props.addPlaylistEntry(
			              this.state.artistChoice.value,
			              this.state.trackChoice.value
		                  )
				  this.setState({artistChoice:{value:'', label:''}});
                                  this.setState({trackChoice:{value:'', label:''}});
		            }
			}
		    />
		</div>
	    );
	}
    }

export {
    Playlist,
    NewPlaylistEntry,
    UsersList
}
