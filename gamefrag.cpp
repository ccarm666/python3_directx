void Game::Draw(float gTime)
{
	int i;
	bool some_face_drawn;
	some_face_drawn = false;
	//Simple RGB value for the background so use XRGB instead of ARGB.
	gDevice->Clear(D3DCOLOR_XRGB(0, 100, 100));
	gDevice->Begin();
	//master_clock = gameTime->totalGameTime; // update masterclock

	if (tobii_menu) tobii_menu->Draw(gTime);
	for (i = 0; i < MAX_NUMBER_OF_BUTTONS + 1; i++) {
		//		tobii_button_matrix[i].button_face->drawIt = true;
		if ((tobii_button_matrix[i].button_face->drawIt && tobii_button_matrix[i].valid_index)) {
			tobii_button_matrix[i].button_face->Draw(gTime);
			some_face_drawn = true;
		}
//		if ((tobii_button_matrix[i].button_face->drawIt && tobii_button_matrix[i].valid_index) && (tobii_button_matrix[i].ssvep_period > 0.0) && 
//			(fmod(gameTime->totalGameTime - tobii_button_matrix[i].face_first_on, tobii_button_matrix[i].ssvep_period) > 
//			(0.5*tobii_button_matrix[i].ssvep_period))) tobii_button_matrix[i].button_face->Draw(gTime);
//		else if ((tobii_button_matrix[i].button_face->drawIt && tobii_button_matrix[i].valid_index) && (tobii_button_matrix[i].ssvep_period == 0.0))
//			tobii_button_matrix[i].button_face->Draw(gTime);

		if (((gameTime->totalGameTime - tobii_button_matrix[i].number_first_on) < tobii_button_matrix[i].number_timer) && tobii_button_matrix[i].valid_index){
			tobii_button_matrix[i].button_num_1->Draw(gTime);
			tobii_button_matrix[i].button_num_2->Draw(gTime);
		}
	}
	gameTime->Update();
	gDevice->End();
	gDevice->Present();
}