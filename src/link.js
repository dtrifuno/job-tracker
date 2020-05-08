import { createHttpLink } from "apollo-link-http";
import { ApolloLink, concat, execute, makePromise } from "apollo-link";
import { onError } from "apollo-link-error";
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

const logoutLink = onError(({ networkError, graphQLErrors }) => {
  if (networkError && networkError.statusCode === 401) {
    console.log("Invalid credentials");
  } else if (graphQLErrors) {
    graphQLErrors.forEach((error) =>
      store.dispatch("flashError", error.message)
    );
  }
});

//const link = logoutLink.concat(httpLink.concat(authMiddleware));
const link = logoutLink.concat(concat(authMiddleware, httpLink));
const executeString = (query, variables) => {
  console.log(query);
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

export const doMutation = (mutationString, variables = {}) => {
  return executeString(
    `mutation {
    ${mutationString}
  }`,
    variables
  );
};

const objectToArgsString = (object) => {
  return (
    Object.entries(object)
      .map((x) => `${x[0]}: $${x[0]}`)
      //      ([field, value]) => `${field}: $${field}`
      //        `${field}: ${typeof value === "string" ? `"${value.replace(/(\r\n|\r|\n)/, "\\n")}"` : `${value}`}`
      //    )
      .join(",\n")
  );
};

const objectToQueryString = (object) => {
  return Object.entries(object)
    .map((x) => `${x[0]}`)
    .join(",\n");
};

export const doMutationFromObject = (
  mutationName,
  mutationObject,
  queryName,
  queryObject
) => {
  return executeString(
    `mutation ${mutationName}() {
       ${mutationName}(${objectToArgsString(mutationObject)}) {
       ${queryName} { ${objectToQueryString(queryObject)} }
    }}`,
    mutationObject
  );
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

export const doDelete = (mutationName, id) => {
  return doMutation(`${mutationName}(id: "${id}") { ok }`);
};

export default doQuery;
