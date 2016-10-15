json.array!(@industries) do |industry|
  json.extract! industry, :id, :name, :active
  json.url industry_url(industry, format: :json)
end
