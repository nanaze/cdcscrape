import plotly.graph_objects as go
import plotly.io
import scrape_test_page
import sys

def _get_column(records, index : int):
  for r in records:
    yield r[index]

def process_records(records):
  total = 0
  for record in records:
    date, cdc, non_cdc = record
    tests = cdc + non_cdc
    total += tests
    yield date, total
    
def main():
  records = list(scrape_test_page.get_records())
  pairs = list(process_records(records))
  fig = go.Figure()
  fig.add_trace(go.Scatter(
    name = 'number of tests performed',
      x=list(p[0] for p in pairs),
      y=list(p[1] for p in pairs)))
  fig.update_layout(
    title='Cumulative CDC-reported tests performed in US by date',
    annotations=[
        dict(
            x=1,
            y=0,
            yshift=-70,
            showarrow=False,
            text="Data from <a href='https://www.cdc.gov/coronavirus/2019-ncov/testing-in-us.html'>CDC</a>. See <a href='http://github.com/nanaze/cdcscript for source'>source</a>.",
            xref="paper",
            yref="paper",
            bordercolor='black',
            borderwidth=1
        ),
    ])
  plotly.io.write_html(fig, sys.stdout)

if __name__ == '__main__':
  main()
