package edu.mit.mitmobile2;

import edu.mit.mitmobile2.about.BuildSettings;
import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;


public class SectionHeader extends FrameLayout {
	private TextView mTextView;
	private ImageView mBackgroundView;
	
	public enum Prominence {
		PRIMARY,
		SECONDARY
	}
	
	public SectionHeader(Context context, AttributeSet attributeSet) {
			super(context, attributeSet);
			
			String initialText = attributeSet.getAttributeValue("http://schemas.android.com/apk/res/android", "text");
			int prominenceInt = attributeSet.getAttributeIntValue("http://schemas.android.com/apk/res/" + BuildSettings.release_project_name, "prominence", 0);
			Prominence prominence = Prominence.values()[prominenceInt];
			initializeHelper(context, initialText, prominence);
	}
	
	public SectionHeader(Context context, String initialText) {
		super(context);
		initializeHelper(context, initialText, Prominence.PRIMARY);
	}
	
	public SectionHeader(Context context, String initialText, Prominence prominence) {
		super(context);
		initializeHelper(context, initialText, prominence);
	}
	
	public void setBackgroundResourceId(int resourceId) {
		mBackgroundView.setImageResource(resourceId);
	}
	
	private void initializeHelper(Context context, String initialText, Prominence prominence) {
		LayoutInflater inflator = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		inflator.inflate(R.layout.section_header, this);
		
		mTextView = (TextView) findViewById(R.id.sectionHeaderTV);
		mTextView.setText(initialText);
		
		mBackgroundView = (ImageView) findViewById(R.id.sectionHeaderBackgroundIV);
		
		if(prominence == Prominence.PRIMARY) {
			setBackgroundResourceId(R.drawable.list_subhead);
		} else if(prominence == Prominence.SECONDARY) {
			setBackgroundResourceId(R.drawable.list_subhead_gray);
		}
		
		int height = mBackgroundView.getDrawable().getIntrinsicHeight();
		LayoutParams params = new LayoutParams(ViewGroup.LayoutParams.FILL_PARENT, height);
		findViewById(R.id.sectionHeaderWrapper)
			.setLayoutParams(params);
	}
	
	public void setText(String text) {
		mTextView.setText(text);
	}
	
}

