import gql from 'graphql-tag';

// INSTRUMENT
export const ADD_INSTRUMENT= gql`
  mutation AddInstrument ($name: String!, $keyword: String!, $description: String!, $supplierUid: Int) {
    createInstrument(name: $name, keyword: $keyword, description: $description, supplierUid:$supplierUid)  {
          uid
          name
          description
          keyword
          supplier {
            uid
            name
          }
    }
  }
`;

export const EDIT_INSTRUMENT= gql`
  mutation EditInstrument ($uid: Int!, $name: String!, $keyword: String!, $description: String!, $supplierUid: Int) {
    updateInstrument(uid: $uid, name: $name, keyword: $keyword, description: $description, supplierUid:$supplierUid){
          uid
          name
          description
          keyword
          supplier {
            uid
            name
      }
    }
  }
`;


// METHOD
export const ADD_METHOD= gql`
  mutation AddMethod ($name: String!, $keyword: String!, $description: String!) {
    createMethod(name: $name, keyword:  $keyword, description: $description) {
      uid
      name
      description
      keyword
    }
  }
`;

export const EDIT_METHOD= gql`
  mutation EditMethod ($uid: Int!, $name: String!, $keyword: String!, $description: String!) {
    updateMethod(uid: $uid, name: $name, keyword:  $keyword, description: $description){
        uid
        name
        description
        keyword
    }
  }
`;

