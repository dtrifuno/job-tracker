import { ApolloLink, concat, execute, makePromise } from "apollo-link";
import { onError } from "apollo-link-error";
import { createHttpLink } from "apollo-link-http";
import gql from "graphql-tag";

import store from "./store";

const httpLink = createHttpLink({ uri: "http://localhost:5000/graphql" });

const authMiddleware = new ApolloLink((operation, forward) => {
  operation.setContext(({ headers = {} }) => ({
    headers: {
      ...headers,
      Authorization: `Bearer ${localStorage.getItem("token") || null}`,
    },
  }));

  return forward(operation);
});

const logoutLink = onError(({ graphQLErrors }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(error => {
      if (error.message.includes("Authorization failure")) {
        store.dispatch("flashError", "Invalid token. Please log in again.")
        store.dispatch("logout");
      } else {
        store.dispatch("flashError", error.message)
      }
    })
  }
});

const link = logoutLink.concat(concat(authMiddleware, httpLink));

export const executeString = (query, variables = {}) => {
  const operation = {
    query: gql`
      ${query}
    `,
    variables,
  };

  return makePromise(execute(link, operation)).then((res) => {
    if (!res.errors) {
      return res;
    } else {
      throw res;
    }
  });
};

export const doQuery = (queryString, variables = {}) => {
  return executeString(
    `query {
    ${queryString}
  }`,
    variables
  );
};

// FIXME: extend to deeper queries
const objectToQueryString = (object) => {
  return Object.entries(object)
    .map((x) => `${x[0]}`)
    .join(",\n");
};

export const doCreateFromObject = (objectName, mutationObject) => {
  const capitalizedName =
    objectName.charAt(0).toUpperCase() + objectName.slice(1);
  const inputName = `${objectName}Data`;

  return executeString(
    `mutation Create${capitalizedName}($${inputName}: ${capitalizedName}Input!) {
    create${capitalizedName}(${inputName}: $${inputName}) {
       ${objectName} { ${objectToQueryString({ ...mutationObject, id: null })} }
    }
  }`,
    { [inputName]: mutationObject }
  );
};

export const doEditFromObject = (objectName, id, mutationObject) => {
  const capitalizedName =
    objectName.charAt(0).toUpperCase() + objectName.slice(1);
  const inputName = `${objectName}Data`;

  return executeString(
    `mutation Edit${capitalizedName}($id: ID!, $${inputName}: ${capitalizedName}Input!) {
    edit${capitalizedName}(id: $id, ${inputName}: $${inputName}) {
       ${objectName} { ${objectToQueryString({ ...mutationObject, id: null })} }
    }
  }`,
    { id: id, [inputName]: mutationObject }
  );
};

export const doDelete = (objectName, id) => {
  const capitalizedName =
    objectName.charAt(0).toUpperCase() + objectName.slice(1);

  return executeString(
    `mutation {
      delete${capitalizedName}(id: "${id}") { ok }
    }`)
};

export default doQuery;
