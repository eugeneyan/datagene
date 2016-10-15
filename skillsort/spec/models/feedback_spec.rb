require 'spec_helper'

describe Feedback do
  let(:feedback) { FactoryGirl.build(:feedback) }


  it { should validate_presence_of(:qn1) }
  it { should validate_presence_of(:qn2) }
  it { should validate_presence_of(:qn3) }
  it { should validate_presence_of(:qn4) }
  it { should validate_presence_of(:qn5) }
  it { should validate_presence_of(:qn6) }
  it { should validate_presence_of(:qn7) }


  it 'should not save when feedback values are not valid' do
    (1..7).each { |i| feedback.send("qn#{i}=", nil) }   # Set blank answers for required questions
    feedback.should_not be_valid
    expect { feedback.save }.to change { Feedback.count }.by(0)
  end


  it 'should save when feedback values are valid' do
    feedback = Feedback.new
    (1..7).each { |i| feedback.send("qn#{i}=", 3) }   # Set answer to required questions
    feedback.should be_valid
    expect { feedback.save }.to change { Feedback.count }.by(1)
  end


  it 'should be able to save without the user id' do
  	feedback.user_id = nil
  	expect { feedback.save }.to change { Feedback.count }.by(1)
  end
end
