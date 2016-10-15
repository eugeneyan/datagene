class MainController < ApplicationController

  	
  	def index; end


  	def about; end


  	def about_us; end


  	def privacy_terms; end


  	def feedback; end

  	
  	def feedback_submit
      @feedback = Feedback.new(feedback_params)

      # If user is logged in, record the user id to feedback
      @feedback.user_id = current_user.id if current_user

      if @feedback.save
        redirect_to '/feedback', notice: 'Thank you for your feedback! SortMySkills will be reviewing it to improve your experience!'
      else
        redirect_to '/feedback', notice: 'Sorry an error has occured. Please kindly try again.'
      end
  	end


    private
    # Only allow the white list through.
    def feedback_params
      params.require(:feedback).permit(:qn1, :qn2, :qn3, :qn4, :qn5, :qn6, :qn7, :qn8, :qn9, :qn10, :qn11)
    end
end