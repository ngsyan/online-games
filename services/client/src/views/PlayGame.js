
import { Container, Row, Col } from "shards-react";

import React, { Component } from 'react'
import { connect } from 'react-redux'
import { withRouter } from "react-router";

import { gameActions } from '../redux/games/actions'
// import { appActions } from '../redux/app/actions'

import { requestStatus } from '../utilities/http'

import Config from '../config'

import socketIOClient from "socket.io-client";

import { BattleShipGame } from '../components/games/battle_ship/BattleShipGame'
import Messages from "../components/messages/Messages"

export class PlayGame extends Component {

  constructor (props) {
    super(props);

    this.state = {
      room_id: this.props.match.params.room_id
    }

    // Enter this room
    this.props.enterRoom(this.state.room_id, this.props.history);
  }

  componentDidMount() {

    const  { user, history } = this.props;

    const socket = socketIOClient(Config.GAME_ROOM_SOCKET_ENDPOINT);

    socket.on('connect', function(){
      console.log('SocketIO: Connected to server')
    });

    socket.on('disconnect', function(){
      console.log('SocketIO: Disconnected from server')
    });

    // Process login response
    socket.on('response_login_with_room', function(data){

      console.log(data)

      if (data.status !== requestStatus.SUCCESS) {
        gameActions.enterRoomFailed(history);
      } else {
        console.log('Authorized successfully.')
      }
      
    });

    // Login
    socket.emit('request_login_with_room', {
      'authorization': user.token,
      'room_public_id': this.state.room_id
    })

  }

  render() {

    return (

      <Container fluid className="main-content-container px-4 mt-2">
      <Row>
          <Col md="8">
          <Row>
              <Col>
              <BattleShipGame room={this.state.room_id} history={this.props.history}></BattleShipGame>
              </Col>
          </Row>
          </Col>
          <Col md="4">
              <Messages></Messages>
          </Col>
      </Row>

      </Container>
    )
  }
}

const mapStateToProps = (state) => ({
  user: state.userReducer
})

const mapDispatchToProps = {
  enterRoom: gameActions.enterRoom
}

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(PlayGame))
