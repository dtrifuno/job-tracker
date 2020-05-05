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
const doQuery = (query) => {
  const operation = {
    query: gql`
      ${query}
    `,
  };

  return makePromise(execute(link, operation)).then((res) => {
    if (!res.errors) {
      return res;
    } else {
      throw res;
    }
  });
};
export default doQuery;
