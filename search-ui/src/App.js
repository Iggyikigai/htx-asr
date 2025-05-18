import React from "react";
import {
  SearchProvider,
  SearchBox,
  Results,
  Paging,
  PagingInfo,
  Sorting,
  Facet
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

const connector = new ElasticsearchAPIConnector({
  host: process.env.REACT_APP_ELASTICSEARCH_HOST,
  index: process.env.REACT_APP_ELASTICSEARCH_INDEX,
  apiKey: process.env.REACT_APP_ELASTICSEARCH_API_KEY,
});

const config = {
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
  //search query should only have generated_text for free search
  searchQuery: {
    disjunctiveFacets: ["gender", "age", "accent", "duration"],
    search_fields: {generated_text: { weight : 3}
    },
    result_fields: {
      generated_text: { raw: {}, snippet: { size: 100, fallback: true } },
      duration: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} }
    },
    //filters for gender, age, accent, duration
    facets: {
      gender: { type: "value" },
      age: { type: "value" },
      accent: { type: "value" },
      duration: {
        type: "range",
        ranges: [
          { from: 0, to: 2, name: "0 - 2s" },
          { from: 2, to: 5, name: "2 - 5s" },
          { from: 5, to: 10, name: "5 - 10s" },
          { from: 10, name: "10s+" }
        ]
      }
    }
  }
};

export default function App() {
  return (
    <div className="App">
      <h1>HTX CV Transcription Search</h1>
      <SearchProvider config={config}>
        <Layout
          header={<SearchBox />}
          sideContent={
            <>
              <Facet field="gender" label="Gender" />
              <Facet field="age" label="Age" />
              <Facet field="accent" label="Accent" />
              <Facet field="duration" label="Duration" />
            </>
          }
          bodyHeader={<PagingInfo />}
          bodyContent={
            <Results
              titleField="generated_text"
              resultView={({ result }) => (
                <div className="sui-result">
                  <h3>{result.generated_text?.raw}</h3>
                  <p><strong>Duration:</strong> {result.duration?.raw}s</p>
                  <p><strong>Age:</strong> {result.age?.raw}</p>
                  <p><strong>Gender:</strong> {result.gender?.raw}</p>
                  <p><strong>Accent:</strong> {result.accent?.raw}</p>
                </div>
              )}
            />
          }
          bodyFooter={<Paging />}
        />
      </SearchProvider>
    </div>
  );
}

