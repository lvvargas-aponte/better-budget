import React, { useContext } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { Container, Table } from "react-bootstrap";
import { Context } from "../store/appContext";
import DeleteFriendsModal from "./DeleteFriendsModal";

const FriendsTable = ({ friends }) => {
  const { store, actions } = useContext(Context);

  const handleDeleteFriends = () => {
    actions.showDeleteFriendsModal();
  };

  return (
    <Container className="friends-container">
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Shared Group</th>
          </tr>
        </thead>
        <tbody>
          {friends.map((friend) => (
            <tr key={friend.id}>
              <td>{friend.name}</td>
              <td>{friend.sharedgroup}</td>
              <td>
                <a href="#">
                  <FontAwesomeIcon
                    icon={faTrash}
                    className="icon-lnk"
                    onClick={() => handleDeleteFriends()}
                  />
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      {store.showDeleteFriendsModal && <DeleteFriendsModal />}
    </Container>
  );
};

export default FriendsTable;